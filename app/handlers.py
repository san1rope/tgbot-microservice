from telethon import events
from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetStickerSetRequest
from telethon.tl import types
from telethon.tl.types import UpdateDeleteMessages

from app.api_interface import *
from app.config import Config
from app.utils import Utils as Ut


class HandleEvents:

    @staticmethod
    async def event_new_message(event: events.NewMessage.Event):
        Config.LOGGER.info(f"Handler called. NewMessage. type = {type(event.message)}")
        print(f"{event.message}")

        msg_obj = event.message
        if isinstance(msg_obj.peer_id, types.PeerChannel):
            full_chat = await Config.TG_CLIENT(GetFullChannelRequest(msg_obj.peer_id))
            chat_obj = full_chat.chats[0]
            chat_id = int(f"-100{chat_obj.id}")

            chat_type = "supergroup" if chat_obj.megagroup else "channel"

        elif isinstance(msg_obj.peer_id, types.PeerChat):
            full_chat = await Config.TG_CLIENT(GetFullChatRequest(msg_obj.peer_id.chat_id))
            chat_obj = full_chat.chats[0]
            chat_id = int(f"-{chat_obj.id}")

            chat_type = "chat"

        else:
            return

        sender = await msg_obj.get_sender()
        if (not isinstance(sender, types.User)) or sender.bot:
            return

        try:
            topic_id = msg_obj.reply_to.reply_to_top_id

        except AttributeError:
            topic_id = None

        if not msg_obj.media:
            media = None

        elif isinstance(msg_obj.media, types.MessageMediaPhoto):
            best_size = await Ut.best_photo_size(photo=msg_obj.media.photo)
            media = MediaPhoto(
                file_size=best_size["size_bytes"],
                mime_type="image/jpeg",
                width=best_size["w"],
                height=best_size["h"],
            )

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
                    sticker_set_res = await Config.TG_CLIENT(
                        GetStickerSetRequest(stickerset=attr_sticker.stickerset, hash=0))
                    short_name = getattr(sticker_set_res.set, "short_name", None)

                media = MediaSticker(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    set_name=short_name,
                    emoji=attr_sticker.alt
                )

            elif attr_audio:
                media = MediaAudio(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    duration=attr_audio.duration,
                    is_voice=attr_audio.voice
                )

            elif attr_animated:
                media = MediaVideoGIF(
                    file_size=doc.size,
                    mime_type="image/gif",
                    duration=attr_video.duration,
                    width=attr_video.w,
                    height=attr_video.h,
                    supports_streaming=attr_video.supports_streaming
                )

            elif attr_video:
                media = MediaVideoGIF(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    duration=attr_video.duration,
                    width=attr_video.w,
                    height=attr_video.h,
                    supports_streaming=attr_video.supports_streaming
                )

            elif attr_filename:
                media = MediaDocument(
                    file_size=doc.size,
                    mime_type=doc.mime_type,
                    file_name=attr_filename.file_name
                )

        else:
            return

        try:
            await APIInterface.send_request(
                req_model=MessageCreated(
                    chat_id=chat_id,
                    message_id=msg_obj.id,
                    text=msg_obj.message,
                    message_type=1,
                    topic_id=topic_id,
                    sender=FromUser(
                        id=sender.id,
                        first_name=sender.first_name,
                        username=sender.username,
                        language_code=sender.lang_code
                    ),
                    chat_info=ChatInfo(
                        title=chat_obj.title,
                        username=chat_obj.username,
                        type=chat_type,
                        is_forum=chat_obj.forum,
                        member_count=full_chat.full_chat.participants_count
                    ),
                    timestamp=msg_obj.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    media=media
                )
            )

        except AttributeError as ex:
            print(f"------------- ex = {ex}")
            print(f"msg_obj; type = {type(msg_obj)}; {msg_obj.__dict__}")
            print(f"sender; type = {type(sender)}; {sender}")

    @staticmethod
    async def event_message_edited(event: events.MessageEdited.Event):
        Config.LOGGER.info("Handler called. MessageEdited")

        msg_obj = event.message
        sender = await msg_obj.get_sender()

        if isinstance(msg_obj.peer_id, types.PeerChannel):
            chat_id = int(f"-100{msg_obj.peer_id.channel_id}")

        elif isinstance(msg_obj.peer_id, types.PeerChat):
            chat_id = int(f"-{msg_obj.peer_id.chat_id}")

        else:
            return

        await APIInterface.send_request(
            req_model=MessageEdited(
                message_id=event.message.id,
                chat_id=chat_id,
                sender=FromUser(
                    id=sender.id,
                    first_name=sender.first_name,
                    username=sender.username,
                    language_code=sender.lang_code
                )
            )
        )

    @staticmethod
    async def event_message_deleted(event: events.MessageDeleted.Event):
        Config.LOGGER.info("Handler called. MessageDeleted")

        print(f"event; type={type(event)}; {event}")

        original_upd = event.original_update
        if isinstance(original_upd, types.UpdateDeleteChannelMessages):
            chat_id = int(f"-100{original_upd.channel_id}")

        elif isinstance(original_upd, UpdateDeleteMessages):
            print(f"updateDeleteMessages; {event.__dict__}")

        # await APIInterface.send_request(
        #     req_model=MessageDeleted(
        #         chat_id=original_upd.channel_id
        #     )
        # )

    @staticmethod
    async def event_chat_action(event: events.ChatAction.Event):
        Config.LOGGER.info("Handler called. ChatAction")

        print(f"ChatAction; type={type(event)}. {event}")

        me = await Config.TG_CLIENT.get_me()
        if event.user_id != me.id:
            print("not my id")
            return
