import os
import logging
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Union

from telethon.tl import types

from app.config import Config


class Utils:

    @staticmethod
    async def add_logging(process_id: int, datetime_of_start: Union[datetime, str]) -> Logger:
        if isinstance(datetime_of_start, str):
            file_dir = datetime_of_start

        elif isinstance(datetime_of_start, datetime):
            file_dir = datetime_of_start.strftime(Config.DATETIME_FORMAT)

        else:
            raise TypeError("datetime_of_start must be str or datetime")

        log_filepath = Path(os.path.abspath(f"{Config.LOGGING_DIR}/{file_dir}/{process_id}.txt"))
        log_filepath.parent.mkdir(parents=True, exist_ok=True)
        log_filepath.touch(exist_ok=True)

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - ' + str(
            process_id) + '| %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_filepath, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @staticmethod
    def best_photo_size(photo):
        best = None
        best_pixels = -1

        for s in photo.sizes:
            if isinstance(s, types.PhotoStrippedSize):
                continue  # пропускаємо інлайн-прев'ю

            if isinstance(s, types.PhotoSize):
                w, h = s.w, s.h
                size_bytes = getattr(s, "size", None)
            elif isinstance(s, types.PhotoSizeProgressive):
                w, h = s.w, s.h
                # фактичний розмір файлу — останній елемент
                size_bytes = s.sizes[-1] if s.sizes else None
            else:
                continue

            pixels = (w or 0) * (h or 0)
            if pixels > best_pixels:
                best_pixels = pixels
                best = {"w": w, "h": h, "size_bytes": size_bytes, "obj": s}

        return best  # dict або None
