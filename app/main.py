import asyncio
from datetime import datetime

from aiohttp import ClientSession
from redis.asyncio import Redis
from telethon import events, TelegramClient

from app.api.kafka import KafkaInterface
from app.config import Config
from app.tg.events_catcher import EventsCatcher
from app.utils import Utils as Ut


async def worker():
    await Ut.log("Queue worker has been started!")

    while True:
        await asyncio.sleep(1)
        task = await Config.QUEUE_WORKER.get()
        for retry in range(1, 4):
            try:
                await task
                break

            except Exception as ex:
                print(ex)


async def main():
    datetime_of_start = datetime.now().strftime(Config.DATETIME_FORMAT)
    process_id = 0

    logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=process_id)
    Config.LOGGER = logger
    Config.AIOHTTP_SESSION = ClientSession()
    Config.QUEUE_WORKER = asyncio.Queue()

    loop = asyncio.get_event_loop()
    loop.create_task(Ut.logging_queue())

    Config.TG_CLIENT = TelegramClient(session="work-app", api_id=Config.TG_API_ID, api_hash=Config.TG_API_HASH,
                                      device_model="Desktop", system_version="Windows 11", app_version="6.3")
    await Config.TG_CLIENT.start(phone=Config.PHONE_NUMBER)

    await Ut.log("Client has been connected!")

    Config.REDIS = await Redis(
        host=Config.REDIS_IP, port=6379, db=0, decode_responses=False, socket_keepalive=True,
        password="784512", health_check_interval=15, socket_connect_timeout=5
    )

    await Ut.log("Redis has been initialized!")
    await Ut.load_data_in_redis()

    asyncio.create_task(worker())
    asyncio.create_task(KafkaInterface().start_polling())

    Config.TG_CLIENT.add_event_handler(EventsCatcher.event_new_message, events.NewMessage())
    Config.TG_CLIENT.add_event_handler(EventsCatcher.event_message_edited, events.MessageEdited())
    Config.TG_CLIENT.add_event_handler(EventsCatcher.event_message_deleted, events.MessageDeleted())
    Config.TG_CLIENT.add_event_handler(EventsCatcher.event_chat_action, events.ChatAction())
    Config.TG_CLIENT.add_event_handler(EventsCatcher.event_raw, events.Raw())
    await Ut.log("Event handlers has been registered!")

    await Config.TG_CLIENT.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
