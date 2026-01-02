from typing import Union

from telethon.tl.types import PeerChannel, PeerChat, PeerUser, Config

from app.api.kafka import SendMessageRequest, EditMessageRequest, DeleteMessageRequest, MessagePinRequest, \
    MessageUnpinRequest, SendPhotoRequest, SendAudioRequest, SendVideoRequest, SendDocumentRequest, SendStickerRequest, \
    SendVoiceRequest, SendGIFRequest, CreateTopicRequest, EditTopicRequest, DeleteTopicRequest


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

            )

        except Exception:
            pass

    @staticmethod
    async def edit_message(payload: EditMessageRequest):
        pass

    @staticmethod
    async def delete_message(payload: DeleteMessageRequest):
        pass

    @staticmethod
    async def message_pin(payload: MessagePinRequest):
        pass

    @staticmethod
    async def message_unpin(payload: MessageUnpinRequest):
        pass

    @staticmethod
    async def send_photo(payload: SendPhotoRequest):
        pass

    @staticmethod
    async def send_video(payload: SendVideoRequest):
        pass

    @staticmethod
    async def send_audio(payload: SendAudioRequest):
        pass

    @staticmethod
    async def send_document(payload: SendDocumentRequest):
        pass

    @staticmethod
    async def send_sticker(payload: SendStickerRequest):
        pass

    @staticmethod
    async def send_voice(payload: SendVoiceRequest):
        pass

    @staticmethod
    async def send_gif(payload: SendGIFRequest):
        pass

    @staticmethod
    async def create_topic(payload: CreateTopicRequest):
        pass

    @staticmethod
    async def edit_topic(payload: EditTopicRequest):
        pass

    @staticmethod
    async def delete_topic(payload: DeleteTopicRequest):
        pass
