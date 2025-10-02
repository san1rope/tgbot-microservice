import asyncio
from datetime import datetime

from aiohttp import ClientSession
from telethon import events

from app.config import Config
from app.handlers import HandleEvents
from app.utils import Utils as Ut


async def main():
    datetime_of_start = datetime.now().strftime(Config.DATETIME_FORMAT)
    process_id = 0

    logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=process_id)
    Config.LOGGER = logger
    Config.AIOHTTP_SESSION = ClientSession()

    Config.TG_CLIENT.add_event_handler(HandleEvents.event_new_message, events.NewMessage())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_message_deleted, events.MessageDeleted())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_message_edited, events.MessageEdited())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_chat_action, events.ChatAction())
    # Config.TG_CLIENT.add_event_handler(HandleEvents.event_raw, events.Raw())

    await Config.TG_CLIENT.start(phone=Config.PHONE_NUMBER)
    await Config.TG_CLIENT.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
