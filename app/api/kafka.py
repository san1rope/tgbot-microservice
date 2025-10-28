import json

from aiokafka import AIOKafkaConsumer
from pydantic import BaseModel
from telethon.tl.functions.channels import EditPhotoRequest

from app.config import Config
from app.tg.actions import UserActions
from app.utils import Utils as Ut


class KafkaInterface:

    @staticmethod
    async def coroutine_from_payload(payload):
        rt = payload.get("request_type")
        if not rt:
            return None

        rt.pop("request_type")
        if rt == "send_message":
            return UserActions.send_message(SendMessageRequest(**payload))

        elif rt == "edit_message":
            return UserActions.edit_message(EditMessageRequest(**payload))

        elif rt == "delete_message":
            return UserActions.delete_message(DeleteMessageRequest(**payload))

        elif rt == "message_pin":
            return UserActions.message_pin(MessagePinRequest(**payload))

        elif rt == "message_unpin":
            return UserActions.message_unpin(MessageUnpinRequest(**payload))

        elif rt == "send_photo":
            return UserActions.send_photo(SendPhotoRequest(**payload))

        elif rt == "send_video":
            return UserActions.send_video(SendVideoRequest(**payload))

        elif rt == "send_audio":
            return UserActions.send_audio(SendAudioRequest(**payload))

        elif rt == "send_document":
            return UserActions.send_document(SendDocumentRequest(**payload))

        elif rt == "send_sticker":
            return UserActions.send_sticker(SendStickerRequest(**payload))

        elif rt == "send_voice":
            return UserActions.send_voice(SendVoiceRequest(**payload))

        elif rt == "send_gif":
            return UserActions.send_gif(SendGIFRequest(**payload))

        elif rt == "create_topic":
            return UserActions.create_topic(CreateTopicRequest(**payload))

        elif rt == "edit_topic":
            return UserActions.edit_topic(EditTopicRequest(**payload))

        elif rt == "delete_topic":
            return UserActions.delete_topic(DeleteTopicRequest(**payload))

        else:
            return None

    @classmethod
    async def start_polling(cls):
        await Ut.log("Kafka listener has been started!")

        consumer = AIOKafkaConsumer(
            "messages",
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_IP,
            group_id="demo-group",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: v.decode("utf-8"),
        )
        await consumer.start()

        try:
            async for msg in consumer:
                print(f"{msg.topic}:{msg.partition}@{msg.offset} key={msg.key} value={msg.value}")

                payload_coroutine = await cls.coroutine_from_payload(json.loads(msg.value))
                if payload_coroutine:
                    await Config.QUEUE_WORKER.put(payload_coroutine)

        finally:
            await consumer.stop()


class PhotoData(BaseModel):
    width: int
    height: int
    file_size: int


class VideoData(BaseModel):
    width: int
    height: int
    duration: int
    file_size: int


class AudioData(BaseModel):
    duration: int
    title: str
    performer: str
    file_size: int


class DocumentData(BaseModel):
    file_name: str
    mime_type: str
    file_size: int


class StickerData(BaseModel):
    width: int
    height: int
    is_animated: bool
    file_size: int


class VoiceData(BaseModel):
    duration: int
    mime_type: str
    file_size: int


class GIFData(BaseModel):
    width: int
    height: int
    duration: int
    file_size: int


class MediaInfo(BaseModel):
    file_type: str
    file_name: str
    mime_type: str
    file_size: int
    width: int
    height: int
    created_at: str


class SendMessageRequest(BaseModel):
    request_id: str
    chat_id: int
    text: str
    topic_id: int
    parse_mode: str
    disable_notification: bool
    reply_to_message_id: int


class EditMessageRequest(BaseModel):
    request_id: str
    chat_id: int
    message_id: int
    text: str
    parse_mode: str


class DeleteMessageRequest(BaseModel):
    request_id: str
    chat_id: int
    message_id: int


class MessagePinRequest(BaseModel):
    request_id: str
    chat_id: int
    message_id: int


class MessageUnpinRequest(BaseModel):
    request_id: str
    chat_id: int
    message_id: int


class SendPhotoRequest(BaseModel):
    request_id: str
    chat_id: int
    photo: str
    caption: str
    topic_id: int
    parse_mode: str


class SendVideoRequest(BaseModel):
    request_id: str
    chat_id: int
    video: str
    caption: str
    topic_id: int
    parse_mode: str


class SendAudioRequest(BaseModel):
    request_id: str
    chat_id: int
    audio: str
    caption: str
    topic_id: int
    parse_mode: str


class SendDocumentRequest(BaseModel):
    request_id: str
    chat_id: int
    document: str
    caption: str
    topic_id: int
    parse_mode: str


class SendStickerRequest(BaseModel):
    request_id: str
    chat_id: int
    sticker: str
    topic_id: int


class SendVoiceRequest(BaseModel):
    request_id: str
    chat_id: int
    voice: str
    caption: str
    topic_id: int


class SendGIFRequest(BaseModel):
    request_id: str
    chat_id: int
    gif: str
    caption: str
    topic_id: int
    parse_mode: str


class CreateTopicRequest(BaseModel):
    request_id: str
    chat_id: int
    title: str
    icon_color: int


class EditTopicRequest(BaseModel):
    request_id: str
    chat_id: int
    topic_id: int
    title: str


class DeleteTopicRequest(BaseModel):
    request_id: str
    chat_id: int
    topic_id: int
