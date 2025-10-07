import os.path
from logging import Logger
from pathlib import Path
from typing import Optional, List
from asyncio import Queue

from aiohttp import ClientSession
from dotenv import load_dotenv
from redis.asyncio import Redis
from telethon import TelegramClient
from pytz import timezone

load_dotenv()

LOG_LIST: List[str] = []


class Config:
    TG_API_ID = int(os.getenv("TG_API_ID").strip())
    TG_API_HASH = os.getenv("TG_API_HASH").strip()
    TG_CLIENT: Optional[TelegramClient] = None

    DATETIME_FORMAT = os.getenv("DATETIME_FORMAT").strip()
    LOGGING_DIR = Path(os.path.abspath("logs"))
    LOGGER: Optional[Logger] = None

    REDIS_IP: str = os.getenv("REDIS_IP").strip()
    REDIS: Optional[Redis] = None

    BASE_URL: str = os.getenv("BASE_URL").strip()
    AIOHTTP_SESSION: Optional[ClientSession] = None

    PHONE_NUMBER = os.getenv("PHONE_NUMBER").strip()
    IGNORE_CHATS = list(map(int, os.getenv("IGNORE_CHATS").split(',')))

    DEBUG: bool = bool(int(os.getenv("DEBUG").strip()))
    DEBUG_USER_ID = int(os.getenv("DEBUG_USER_ID").strip())
    DEBUG_TIMEZONE = timezone(os.getenv("DEBUG_TIMEZONE").strip())

    QUEUE_EVENTS: Optional[Queue] = None
    QUEUE_CMDS: Optional[Queue] = None

    EVENT_WORKERS_COUNT: int = int(os.getenv("EVENT_WORKERS_COUNT").strip())
    CMD_WORKERS_COUNT: int = int(os.getenv("CMD_WORKERS_COUNT").strip())

    DATABASE_CLEANUP = bool(int(os.getenv("DATABASE_CLEANUP")))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
