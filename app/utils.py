import os
import logging
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Union, Dict, Tuple

from telethon.tl import types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetStickerSetRequest, GetFullChatRequest

from app.api_interface import *
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
    async def get_chat_data_from_peer(peer_id, only_chat_id: bool = False) -> Union[ChatInfo, None]:
        if isinstance(peer_id, types.PeerChannel):
            full_chat = await Config.TG_CLIENT(GetFullChannelRequest(peer_id))
            chat_obj = full_chat.chats[0]
            chat_id = int(f"-100{chat_obj.id}")

            chat_type = "supergroup" if chat_obj.megagroup else "channel"

        elif isinstance(peer_id, types.PeerChat):
            full_chat = await Config.TG_CLIENT(GetFullChatRequest(peer_id.chat_id))
            chat_obj = full_chat.chats[0]
            chat_id = int(f"-{chat_obj.id}")

            chat_type = "chat"

        else:
            return None if only_chat_id else (None, None)

        chat_info = ChatInfo(
            title=chat_obj.title,
            username=chat_obj.username,
            type=chat_type,
            is_forum=chat_obj.forum,
            member_count=full_chat.full_chat.participants_count
        )
        return chat_id if only_chat_id else (chat_id, chat_info)

    @staticmethod
    async def get_topic_data_from_msg(msg_obj: types.Message, only_id: bool = False):
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

    @staticmethod
    async def get_media_data_from_msg(msg_obj: types.Message):
        media = None
        msg_type = 1

        if isinstance(msg_obj.media, types.MessageMediaPhoto):
            best_size = await Utils.best_photo_size(photo=msg_obj.media.photo)
            media = MediaPhoto(
                file_size=best_size["size_bytes"],
                mime_type="image/jpeg",
                width=best_size["w"],
                height=best_size["h"],
            )
            msg_type = 2

        elif isinstance(msg_obj.media, types.MessageMediaDocument):
            doc = msg_obj.media.document

            attr_sticker, attr_video, attr_audio, attr_filename, attr_animated = None, None, None, None, None
            for attr in doc.attributes:
                if isinstance(attr, types.DocumentAttributeSticker):
                    attr_sticker = attr

                elif isinstance(attr, types.DocumentAttributeVideo):
                    attr_video = attr

                elif isinstance(attr, types.DocumentAttributeAudio):
                    attr_audio = attr

                elif isinstance(attr, types.DocumentAttributeFilename):
                    attr_filename = attr

                elif isinstance(attr, types.DocumentAttributeAnimated):
                    attr_animated = attr

            if attr_sticker:
                if isinstance(attr_sticker.stickerset, types.InputStickerSetShortName):
                    short_name = attr_sticker.stickerset.short_name

                else:
                    print(f"stickerset = {attr_sticker.stickerset}")
                    sticker_set_res = await Config.TG_CLIENT(
                        GetStickerSetRequest(stickerset=attr_sticker.stickerset, hash=0))
                    short_name = getattr(sticker_set_res.set, "short_name", None)

                media = MediaSticker(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    set_name=short_name,
                    emoji=attr_sticker.alt
                )
                msg_type = 4

            elif attr_audio:
                media = MediaAudio(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    duration=attr_audio.duration,
                    is_voice=attr_audio.voice
                )
                msg_type = 7

            elif attr_animated:
                media = MediaVideoGIF(
                    file_size=doc.size,
                    mime_type="image/gif",
                    duration=attr_video.duration,
                    width=attr_video.w,
                    height=attr_video.h,
                    supports_streaming=attr_video.supports_streaming
                )
                msg_type = 11

            elif attr_video:
                media = MediaVideoGIF(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    duration=attr_video.duration,
                    width=attr_video.w,
                    height=attr_video.h,
                    supports_streaming=attr_video.supports_streaming
                )
                msg_type = 11

            elif attr_filename:
                media = MediaDocument(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    file_name=attr_filename.file_name
                )
                msg_type = 6

        return msg_type, media
