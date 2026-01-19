import traceback
from typing import Union

from telethon.tl.types import PeerChannel, PeerChat, PeerUser

from app.api.kafka import SendMessageRequest, EditMessageRequest, DeleteMessageRequest, MessagePinRequest, \
    MessageUnpinRequest, SendPhotoRequest, SendAudioRequest, SendVideoRequest, SendDocumentRequest, SendStickerRequest, \
    SendVoiceRequest, SendGIFRequest, CreateTopicRequest, EditTopicRequest, DeleteTopicRequest
from app.config import Config


class UserActions:

    @staticmethod
    async def get_peer_from_id(chat_id: Union[str, int]):
        chat_id = str(chat_id)
        if chat_id.startswith("-100"):
            return PeerChannel(channel_id=int(chat_id[4:]))

        elif chat_id.startswith("-"):
            return PeerChat(chat_id=int(chat_id[1:]))

        else:
            return PeerUser(user_id=int(chat_id))

    @staticmethod
    async def send_message(payload: SendMessageRequest):
        try:
            result = await Config.TG_CLIENT.send_message(
                entity=await UserActions.get_peer_from_id(payload.chat_id),
                message=payload.text,
                parse_mode=payload.parse_mode,
                silent=payload.disable_notification,
                reply_to=payload.topic_id if payload.topic_id else payload.reply_to_message_id
            )
            print(f"result send_message = {result}")

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def edit_message(payload: EditMessageRequest):
        try:
            result = await Config.TG_CLIENT.edit_message(
                entity=await UserActions.get_peer_from_id(payload.chat_id),
                message=payload.message_id,
                text=payload.text,
                parse_mode=payload.parse_mode
            )
            print(f"result edit_message = {result}")

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def delete_message(payload: DeleteMessageRequest):
        try:
            result = await Config.TG_CLIENT.delete_messages(
                entity=await UserActions.get_peer_from_id(payload.chat_id),
                message_ids=payload.message_id
            )
            print(f"result delete_message = {result}")

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def message_pin(payload: MessagePinRequest):
        try:
            result = await Config.TG_CLIENT.pin_message(
                entity=await UserActions.get_peer_from_id(payload.chat_id),
                message=payload.message_id
            )
            print(f"result message_pin = {result}")

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def message_unpin(payload: MessageUnpinRequest):
        try:
            result = await Config.TG_CLIENT.unpin_message(
                entity=await UserActions.get_peer_from_id(payload.chat_id),
                message=payload.message_id
            )
            print(f"result message_unpin = {result}")

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def send_photo(payload: SendPhotoRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def send_video(payload: SendVideoRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def send_audio(payload: SendAudioRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def send_document(payload: SendDocumentRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def send_sticker(payload: SendStickerRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def send_voice(payload: SendVoiceRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def send_gif(payload: SendGIFRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def create_topic(payload: CreateTopicRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def edit_topic(payload: EditTopicRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())

    @staticmethod
    async def delete_topic(payload: DeleteTopicRequest):
        try:
            pass

        except Exception:
            print(traceback.format_exc())
