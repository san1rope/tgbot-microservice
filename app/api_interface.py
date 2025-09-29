from typing import Union, List, Optional
from venv import logger

from aiohttp import ClientSession
from pydantic import BaseModel

from app.config import Config


class FromUser(BaseModel):
    id: int
    first_name: str
    username: Optional[str] = None
    language_code: Optional[str] = None


class ChatInfo(BaseModel):
    title: str
    username: Optional[str]
    type: str
    is_forum: bool
    member_count: int


class MediaPhoto(BaseModel):
    type_name: str = "photo"
    file_size: int
    mime_type: str
    width: int
    height: int


class MediaSticker(BaseModel):
    type_name: str = "sticker"
    file_size: int
    mime_type: str
    emoji: str
    set_name: str


class MediaDocument(BaseModel):
    type_name: str = "document"
    file_size: int
    mime_type: str
    file_name: str


class MediaAudio(BaseModel):
    type_name: str = "audio_voice"
    file_size: int
    mime_type: str
    duration: int
    is_voice: bool


class MediaVideoGIF(BaseModel):
    type_name: str = "video_gif"
    file_size: int
    mime_type: str
    duration: float
    width: int
    height: int
    supports_streaming: bool


class MessageCreated(BaseModel):
    type: str = "message_created"
    chat_id: int
    message_id: int
    text: Optional[str] = None
    message_type: int = 1
    topic_id: Optional[int] = None
    sender: FromUser
    chat_info: ChatInfo
    timestamp: str
    media: Union[None, MediaPhoto, MediaSticker, MediaDocument, MediaAudio, MediaVideoGIF]


class MessageEdited(BaseModel):
    message_id: int
    chat_id: int
    sender: FromUser


class MessageDeleted(BaseModel):
    type: str = "message_deleted"
    chat_id: int
    message_ids: List[int]
    topic_id: int
    deleted_by: FromUser
    chat_info: ChatInfo
    timestamp: str


class TopicCreated(BaseModel):
    type: str = "topic_created"
    chat_id: int
    topic_id: int
    title: str
    icon_color: int
    created_by: FromUser
    chat_info: ChatInfo
    timestamp: str


class BotAdded(BaseModel):
    type: str = "bot_added_to_chat"
    chat_id: int
    chat_info: ChatInfo
    owner_info: FromUser
    added_by: FromUser
    timestamp: str


class APIInterface:

    @staticmethod
    async def send_request(req_model: Union[MessageCreated, MessageEdited, MessageDeleted, TopicCreated, BotAdded]):
        if not Config.AIOHTTP_SESSION:
            Config.AIOHTTP_SESSION = ClientSession()

        print(f"req_model = {req_model}")

        url = Config.BASE_URL
        if isinstance(req_model, MessageCreated):
            url += "/webhook/telegram/create"

        elif isinstance(req_model, MessageEdited):
            url += "/webhook/telegram/update"

        elif isinstance(req_model, MessageDeleted):
            url += "/webhook/telegram/delete"

        elif isinstance(req_model, TopicCreated):
            url += "/webhook/telegram/topic_created"

        elif isinstance(req_model, BotAdded):
            url += "/webhook/telegram/bot_added"

        else:
            return TypeError

        headers = {
            "Content-Type": "application/json"
        }

        async with Config.AIOHTTP_SESSION.post(
                url=url, headers=headers, json=req_model.model_dump(), timeout=15) as response:
            answer = await response.json()
            logger.info(f"{response.status} | {url} | {answer}")

        return answer
