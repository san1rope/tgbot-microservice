import asyncio

from telethon import TelegramClient
from telethon.tl.types import PeerChat

from app.config import Config


async def main():
    Config.TG_CLIENT = TelegramClient(session="work-app", api_id=Config.TG_API_ID, api_hash=Config.TG_API_HASH)
    await Config.TG_CLIENT.start(phone=Config.PHONE_NUMBER)

    entity = PeerChat(chat_id=4907822179)
    result = await Config.TG_CLIENT.send_message(
        entity=entity,
        message="abc",
        parse_mode="markdown",
        silent=True
    )
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
