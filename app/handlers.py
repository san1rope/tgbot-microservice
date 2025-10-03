from telethon import events

from app.api_interface import *
from app.config import Config
from app.utils import Utils as Ut


class HandleEvents:

    @staticmethod
    async def event_new_message(event: events.NewMessage.Event):
        Config.LOGGER.info(f"Handler called. NewMessage. type = {type(event.message)}")
        msg_obj = event.message

        sender = await msg_obj.get_sender()
        from_user = await FromUser.obj_from_sender(sender)
        if not from_user:
            return

        chat_id, chat_info = await Ut.get_chat_data_from_peer(msg_obj.peer_id)
        if not chat_id:
            return

        msg_timestamp = msg_obj.date.strftime("%Y-%m-%dT%H:%M:%SZ")

        topic_id, title, icon_color = await Ut.get_topic_data_from_msg(msg_obj)
        if topic_id and (topic_id + 1 == msg_obj.id):
            await APIInterface.send_request(
                req_model=TopicCreated(
                    chat_id=chat_id,
                    topic_id=topic_id,
                    title=title,
                    icon_color=icon_color,
                    created_by=from_user,
                    chat_info=chat_info,
                    timestamp=msg_timestamp
                )
            )

        msg_type, media = await Ut.get_media_data_from_msg(msg_obj)

        try:
            await APIInterface.send_request(
                req_model=MessageCreated(
                    chat_id=chat_id,
                    message_id=msg_obj.id,
                    text=msg_obj.message,
                    message_type=msg_type,
                    topic_id=topic_id,
                    sender=from_user,
                    chat_info=chat_info,
                    timestamp=msg_timestamp,
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

        chat_id, chat_info = await Ut.get_chat_data_from_peer(msg_obj.peer_id)
        if not chat_id:
            return

        sender = await msg_obj.get_sender()
        from_user = await FromUser.obj_from_sender(sender)
        if not from_user:
            return

        msg_type, media = await Ut.get_media_data_from_msg(msg_obj)

        await APIInterface.send_request(
            req_model=MessageEdited(
                chat_id=chat_id,
                message_id=msg_obj.id,
                text=msg_obj.message,
                message_type=1,
                sender=from_user,
                chat_info=chat_info,
                timestamp=msg_obj.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                media=media
            )
        )

    @staticmethod
    async def event_message_deleted(event: events.MessageDeleted.Event):
        Config.LOGGER.info("Handler called. MessageDeleted")

        print(f"event; type={type(event)}; {event}")

        return

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

    @staticmethod
    async def event_raw(event):
        print(f"raw; type={type(event)}; {event}")

        if isinstance(event, types.UpdateNewChannelMessage):
            action = event.message.action
            if not action:
                return None

            if isinstance(action, types.MessageActionTopicEdit):
                peer_id = event.message.peer_id
                if isinstance(peer_id, types.PeerChannel):
                    chat_id = int(f"-100{peer_id.channel_id}")

                elif isinstance(peer_id, types.PeerChat):
                    chat_id = int(f"-{peer_id.chat_id}")

                else:
                    return None

                return await APIInterface.send_request(
                    req_model=TopicEdited(
                        topic_id=1,
                        chat_id=chat_id,
                        title=action.title
                    )
                )

        return None
