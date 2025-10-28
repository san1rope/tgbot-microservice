from app.api.kafka import *


class UserActions:

    @staticmethod
    async def send_message(payload: SendMessageRequest):
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
