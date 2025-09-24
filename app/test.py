import asyncio
from datetime import datetime

from aiohttp import ClientSession
from telethon import events

from app.api_interface import MessageCreated, FromUser, ChatInfo, APIInterface
from app.config import Config
from app.utils import Utils as Ut

# @Config.TG_CLIENT.on(events.NewMessage)
# async def new_message_handler(event):
#     print(event)
#
#
# async def main():
#     datetime_of_start = datetime.now().strftime(Config.DATETIME_FORMAT)
#     process_id = 0
#
#     logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=process_id)
#     Config.LOGGER = logger
#
#     await Config.TG_CLIENT.start(phone="+380661677548")
#     await Config.TG_CLIENT.run_until_disconnected()


async def main():
    req_model = MessageCreated(
        chat_id=-1001234567890,
        message_id=123456,
        text="new message text",
        message_type=1,
        topic_id=67893,
        sender=FromUser(
            id=129381293,
            first_name="John",
            username="djqowq",
            language_code="en"
        ),
        chat_info=ChatInfo(
            title="test group",
            username="aodjoaewd",
            type="supergroup",
            member_count=102,
            is_forum=True
        ),
        timestamp="2025-09-24T14:21:06Z",
        media=None
    )

    # data = {
    #     "type": "message_created",
    #     "chat_id": -1001234567890,
    #     "message_id": 12345,
    #     "text": "Привет, это новое сообщение!",
    #     "message_type": 1,
    #     "topic_id": 67890,
    #     "sender": {
    #         "id": 123456789,
    #         "first_name": "Иван",
    #         "username": "ivan_user",
    #         "language_code": "ru"
    #     },
    #     "chat_info": {
    #         "title": "Тестовая группа",
    #         "username": "test_group",
    #         "type": "supergroup",
    #         "is_forum": True,
    #         "member_count": 150
    #     },
    #     "timestamp": "2025-09-05T10:01:00Z",
    #     "media": None
    # }

    result = await APIInterface.send_request(req_model)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
