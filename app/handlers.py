from telethon import events
from telethon.events import NewMessage
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import PeerChannel, PeerChat, MessageMediaDocument

from app.api_interface import APIInterface, MessageCreated, FromUser, ChatInfo, MediaDocument
from app.config import Config


class HandleEvents:

    @staticmethod
    async def event_new_message(event: NewMessage.Event):
        Config.LOGGER.info(f"Handler called. NewMessage. type = {type(event.message)}")

        msg_obj = event.message
        if isinstance(msg_obj.peer_id, PeerChannel):
            full_chat = await Config.TG_CLIENT(GetFullChannelRequest(msg_obj.peer_id))
            chat_obj = full_chat.chats[0]
            chat_id = int(f"-100{chat_obj.id}")

            chat_type = "supergroup" if chat_obj.megagroup else "channel"

        elif isinstance(msg_obj.peer_id, PeerChat):
            full_chat = await Config.TG_CLIENT(GetFullChatRequest(msg_obj.peer_id))
            chat_obj = full_chat.chats[0]
            chat_id = int(f"-{chat_obj.id}")

            chat_type = "chat"

        else:
            return

        sender = await msg_obj.get_sender()
        if sender.bot:
            return

        try:
            topic_id = msg_obj.reply_to.reply_to_top_id

        except AttributeError:
            topic_id = None

        if not msg_obj.media:
            media = None

        elif isinstance(msg_obj.media, MessageMediaDocument):
            print(f"size = {msg_obj.media.document.size}")

            media = MediaDocument(
                file_size=msg_obj.media.document.size,
                file_name=
            )

        else:
            print(f"media; type={type(msg_obj.media)}; {msg_obj.media}")

        # try:
        #     await APIInterface.send_request(
        #         req_model=MessageCreated(
        #             chat_id=chat_id,
        #             message_id=msg_obj.id,
        #             text=msg_obj.message,
        #             message_type=1,
        #             topic_id=topic_id,
        #             sender=FromUser(
        #                 id=sender.id,
        #                 first_name=sender.first_name,
        #                 username=sender.username,
        #                 language_code=sender.lang_code
        #             ),
        #             chat_info=ChatInfo(
        #                 title=chat_obj.title,
        #                 username=chat_obj.username,
        #                 type=chat_type,
        #                 is_forum=chat_obj.forum,
        #                 member_count=full_chat.full_chat.participants_count
        #             ),
        #             timestamp=msg_obj.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        #             media=None
        #         )
        #     )
        #
        # except AttributeError as ex:
        #     print(f"------------- ex = {ex}")
        #     print(f"msg_obj; type = {type(msg_obj)}; {msg_obj.__dict__}")
        #     print(f"sender; type = {type(sender)}; {sender}")

    @staticmethod
    async def event_message_deleted(event):
        Config.LOGGER.info("Handler called. MessageDeleted")
