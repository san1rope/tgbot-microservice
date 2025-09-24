import asyncio
from datetime import datetime

from aiohttp import ClientSession

from app.config import Config
from app.utils import Utils as Ut


async def main():
    datetime_of_start = datetime.now().strftime(Config.DATETIME_FORMAT)
    process_id = 0

    logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=process_id)
    Config.LOGGER = logger
    Config.AIOHTTP_SESSION = ClientSession()


if __name__ == "__main__":
    asyncio.run(main())
