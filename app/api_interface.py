from typing import Union, List

from aiohttp import ClientSession
from pydantic import BaseModel

from app.config import Config


class FromUser(BaseModel):
    id: int
    first_name: str
    username: str
    language_code: str


class ChatInfo(BaseModel):
    title: str
    username: str
    type: str
    is_forum: bool
    member_count: int


class MediaPhoto(BaseModel):
    type_name: str = "photo"
    file_size: int
    mime_type: str = "image/jpeg"
    width: int
    height: int


class MediaSticker(BaseModel):
    type_name: str = "sticker"
    file_size: int
    mime_type: str = "image/webp"
    emoji: str
    set_name: str


class MediaDocument(BaseModel):
    type_name: str = "document"
    file_size: int
    mime_type: str = "application/pdf"
    file_name: str


class MediaAudioVoice(BaseModel):
    type_name: str = "audio_voice"
    file_size: int
    mime_type: str = "audio/ogg"
    duration: int
    is_voice: bool


class MediaVideoGIF(BaseModel):
    type_name: str = "video_gif"
    file_size: int
    mime_type: str = "video/mp4"
    duration: int
    width: int
    height: int
    supports_streaming: bool


class MessageCreated(BaseModel):
    type: str = "message_created"
    chat_id: int
    message_id: int
    text: str
    message_type: int = 1
    topic_id: int
    sender: FromUser
    chat_info: ChatInfo
    timestamp: str
    media: Union[None, MediaPhoto, MediaSticker, MediaDocument, MediaAudioVoice, MediaVideoGIF]


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

    # @staticmethod
    # async def send_request(req_model:  Union[]):

    @staticmethod
    async def create_message(model: MessageCreated):
        if not Config.AIOHTTP_SESSION:
            Config.AIOHTTP_SESSION = ClientSession()

        url = Config.BASE_URL + "/webhook/telegram/create"
        headers = {
            "Content-Type": "application/json"
        }

        async with Config.AIOHTTP_SESSION.post(
                url=url, headers=headers, json=model.model_dump(), timeout=15) as response:
            answer = await response.json()

        return answer

    @staticmethod
    async def delete_message(model: MessageDeleted):
        if not Config.AIOHTTP_SESSION:
            Config.AIOHTTP_SESSION = ClientSession()

        url = Config.BASE_URL + "/webhook/telegram/delete"
        headers = {
            "Content-Type": "application/json"
        }

        async with Config.AIOHTTP_SESSION.post(
                url=url, headers=headers, json=model.model_dump(), timeout=15) as response:
            answer = await response.json()

        return answer

    @staticmethod
    async def create_topic(model: TopicCreated):
        if not Config.AIOHTTP_SESSION:
            Config.AIOHTTP_SESSION = ClientSession()

        url = Config.BASE_URL + "/webhook/telegram/topic_created"
        headers = {
            "Content-Type": "application/json"
        }

        async with Config.AIOHTTP_SESSION.post(
                url=url, headers=headers, json=model.model_dump(), timeout=15) as response:
            answer = await response.json()

        return answer
