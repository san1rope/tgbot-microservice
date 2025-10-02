import os
import logging
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Union, Dict

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
    async def best_photo_size(photo) -> Union[Dict, None]:
        best = None
        best_pixels = -1

        for s in photo.sizes:
            if isinstance(s, types.PhotoStrippedSize):
                continue

            if isinstance(s, types.PhotoSize):
                w, h = s.w, s.h
                size_bytes = getattr(s, "size", None)
            elif isinstance(s, types.PhotoSizeProgressive):
                w, h = s.w, s.h
                size_bytes = s.sizes[-1] if s.sizes else None
            else:
                continue

            pixels = (w or 0) * (h or 0)
            if pixels > best_pixels:
                best_pixels = pixels
                best = {"w": w, "h": h, "size_bytes": size_bytes}

        return best

    @staticmethod
    async def get_chat_id_from_peer(peer_id) -> Union[int]:
        if isinstance(peer_id, types.PeerChannel):
            chat_id = int(f"-100{peer_id.channel_id}")

        elif isinstance(peer_id, types.PeerChat):
            chat_id = int(f"-{peer_id.chat_id}")

        else:
            chat_id = 0

        return chat_id

    @staticmethod
    async def get_topic_info_from_msg(msg_obj: types.Message, only_id: bool = False):
        topic_id = None
        title = ""
        icon_color = 0
        if isinstance(msg_obj.reply_to, types.MessageReplyHeader) and msg_obj.reply_to.forum_topic:
            topic_id = msg_obj.reply_to.reply_to_top_id if msg_obj.reply_to.reply_to_top_id \
                else msg_obj.reply_to.reply_to_msg_id

            topic_msg = await Config.TG_CLIENT.get_messages(msg_obj.peer_id, ids=topic_id)
            if isinstance(topic_msg, types.MessageService) and \
                    isinstance(topic_msg.action, types.MessageActionTopicCreate):
                title = topic_msg.action.title
                icon_color = topic_msg.action.icon_color

        if only_id:
            return topic_id

        return topic_id, title, icon_color
