import asyncio
from datetime import datetime

from aiohttp import ClientSession
from redis.asyncio import Redis
from telethon import events

from app.config import Config
from app.tg.events_catcher import EventsCatcher
from app.utils import Utils as Ut


async def worker_events():
    await Ut.log("Events worker has been started!")

    while True:
        await asyncio.sleep(1)
        try:
            task = await Config.QUEUE_EVENTS.get()
            for retry in range(1, 4):
                result = await task
                if result:
                    break

                else:
                    await Ut.log(f"Не удалось завершить event задачу! Осталось попыток: {retry}")

        except Exception as ex:
            pass


async def worker_cmds():
    await Ut.log("Commands worker has been started!")

    while True:
        await asyncio.sleep(1)
        try:
            task = await Config.QUEUE_CMDS.get()
            for retry in range(1, 4):
                result = await task
                if result:
                    break

                else:
                    await Ut.log(f"Не удалось завершить cmd задачу! Осталось попыток: {retry}")

        except Exception as ex:
            pass


async def main():
    datetime_of_start = datetime.now().strftime(Config.DATETIME_FORMAT)
    process_id = 0

    logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=process_id)
    Config.LOGGER = logger
    Config.AIOHTTP_SESSION = ClientSession()
    Config.QUEUE_EVENTS = asyncio.Queue()
    Config.QUEUE_CMDS = asyncio.Queue()

    loop = asyncio.get_event_loop()
    loop.create_task(Ut.logging_queue())

    await Config.TG_CLIENT.start(phone=Config.PHONE_NUMBER)
    await Ut.log("Client has been connected!")

    Config.REDIS = await Redis(
        host="192.168.26.153", port=6379, db=0, decode_responses=False, socket_keepalive=True,
        password="784512", health_check_interval=15, socket_connect_timeout=5
    )
    await Ut.log("Redis has been initialized!")
    await Ut.load_data_in_redis()

    asyncio.create_task(worker_events())
    asyncio.create_task(worker_cmds())

    Config.TG_CLIENT.add_event_handler(EventsCatcher.event_new_message, events.NewMessage())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_message_edited, events.MessageEdited())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_message_deleted, events.MessageDeleted())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_chat_action, events.ChatAction())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_raw, events.Raw())
    await Ut.log("Event handlers has been registered!")

    await Config.TG_CLIENT.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
