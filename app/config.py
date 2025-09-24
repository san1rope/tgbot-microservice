import os.path
from logging import Logger
from pathlib import Path
from typing import Optional

from aiohttp import ClientSession
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()


class Config:
    TG_API_ID = int(os.getenv("TG_API_ID").strip())
    TG_API_HASH = os.getenv("TG_API_HASH").strip()
    TG_CLIENT = TelegramClient(session="work-app", api_id=TG_API_ID, api_hash=TG_API_HASH)

    DATETIME_FORMAT = os.getenv("DATETIME_FORMAT").strip()
    LOGGING_DIR = Path(os.path.abspath("logs"))
    LOGGER: Optional[Logger] = None

    BASE_URL: str = os.getenv("BASE_URL").strip()
    AIOHTTP_SESSION: Optional[ClientSession] = None
