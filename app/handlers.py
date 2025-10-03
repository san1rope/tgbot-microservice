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

        chat_id, chat_info = await ChatInfo.obj_from_peer(msg_obj.peer_id)
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

        chat_id, chat_info = await ChatInfo.obj_from_peer(msg_obj.peer_id)
        if not chat_id:
            return

        sender = await msg_obj.get_sender()
        from_user = await FromUser.obj_from_sender(sender)
        if not from_user:
            return

        msg_type, media = await Ut.get_media_data_from_msg(msg_obj)
        topic_id = await Ut.get_topic_data_from_msg(msg_obj, only_id=True)

        await APIInterface.send_request(
            req_model=MessageEdited(
                chat_id=chat_id,
                message_id=msg_obj.id,
                text=msg_obj.message,
                message_type=msg_type,
                topic_id=topic_id,
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

        # original_upd = event.original_update
        # if isinstance(original_upd, types.UpdateDeleteChannelMessages):
        #     chat_id = int(f"-100{original_upd.channel_id}")
        #
        # elif isinstance(original_upd, UpdateDeleteMessages):
        #     print(f"updateDeleteMessages; {event.__dict__}")

        # await APIInterface.send_request(
        #     req_model=MessageDeleted(
        #         chat_id=original_upd.channel_id
        #     )
        # )

    @staticmethod
    async def event_chat_action(event: events.ChatAction.Event):
        Config.LOGGER.info("Handler called. ChatAction")

        print(f"ChatAction; {event}")

        me = await Config.TG_CLIENT.get_me()
        act_msg = event.action_message
        if isinstance(act_msg.action, types.MessageActionChatAddUser) and (me.id in act_msg.action.users):
            chat_id, chat_info = await ChatInfo.obj_from_peer(act_msg.peer_id)
            if not chat_id:
                return

            added_by_user = await Config.TG_CLIENT.get_entity(act_msg.from_id)
            added_by = await FromUser.obj_from_sender(added_by_user)
            if not added_by:
                return

            owner_user = await Config.TG_CLIENT.get_entity()
            owner_info = await FromUser.obj_from_sender(owner_user)
            if not owner_info:
                return

            chat_entity = await Config.TG_CLIENT.get_entity(act_msg.peer_id)


            await APIInterface.send_request(
                req_model=BotAdded(
                    chat_id=chat_id,
                    chat_info=chat_info,
                    owner_info=owner_info,
                    added_by=added_by,
                    timestamp=act_msg.date.strftime("%Y-%m-%dT%H:%M:%SZ")
                )
            )

    @staticmethod
    async def event_raw(event):
        if isinstance(event, types.UpdateNewChannelMessage):
            action = event.message.action
            if not action:
                return None

            if isinstance(action, types.MessageActionTopicEdit):
                Config.LOGGER.info(f"Handler called. TopicEdited: {type(action)}")
                msg_obj = event.message

                sender = await Config.TG_CLIENT.get_entity(msg_obj.from_id)
                from_user = await FromUser.obj_from_sender(sender)
                if not from_user:
                    return None

                chat_id, chat_info = await ChatInfo.obj_from_peer(msg_obj.peer_id)
                if not chat_id:
                    return None

                topic_id, title, icon_color = await Ut.get_topic_data_from_msg(msg_obj)

                return await APIInterface.send_request(
                    req_model=TopicEdited(
                        chat_id=chat_id,
                        topic_id=topic_id,
                        title=title,
                        icon_color=icon_color,
                        sender=from_user,
                        chat_info=chat_info,
                        timestamp=msg_obj.date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    )
                )

        return None
