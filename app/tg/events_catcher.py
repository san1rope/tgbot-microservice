from typing import Union

from telethon import events
from telethon.tl import types

from app.config import Config
from app.tg.handlers import HandleEvents
from app.tg.tg_tools import TgTools


class EventsCatcher:

    @staticmethod
    async def check_chat_id(chat_id: Union[int, types.PeerChat, types.PeerChannel, types.PeerUser]) -> bool:
        if isinstance(chat_id, types.PeerChat):
            chat_id = int(f"-{chat_id.chat_id}")

        elif isinstance(chat_id, types.PeerChannel):
            chat_id = int(f"-100{chat_id.channel_id}")

        else:
            return False

        if chat_id in Config.IGNORE_CHATS:
            return False

        return True

    @staticmethod
    async def event_new_message(event: events.NewMessage.Event):
        if not await EventsCatcher.check_chat_id(event.message.peer_id):
            return

        topic_id = await TgTools.get_topic_data_from_msg(msg_obj=event.message, only_id=True)
        if topic_id and (topic_id + 1 == event.message.id):
            await Config.QUEUE_EVENTS.put(HandleEvents.processing_new_message(event))

        else:
            await Config.QUEUE_EVENTS.put(HandleEvents.processing_create_topic(event))

    @staticmethod
    async def event_message_edited(event: events.MessageEdited.Event):
        if await EventsCatcher.check_chat_id(event.message.peer_id):
            await Config.QUEUE_EVENTS.put(HandleEvents.processing_message_edited(event))

    @staticmethod
    async def event_message_deleted(event: events.MessageDeleted.Event):
        org_upd = event.original_update
        if isinstance(org_upd, types.UpdateDeleteChannelMessages):
            chat_id = org_upd.channel_id

        elif isinstance(org_upd, types.UpdateDeleteMessages):
            chat_id = None
            for msg_id in org_upd.messages:
                chat_id = int(await Config.REDIS.get(f"msg:{msg_id}"))
                if chat_id:
                    break

            if not chat_id:
                return

        else:
            return

        if await EventsCatcher.check_chat_id(chat_id):
            await Config.QUEUE_EVENTS.put(HandleEvents.processing_message_deleted(event))

    @staticmethod
    async def event_chat_action(event: events.ChatAction.Event):
        act_msg = event.action_message
        if not await EventsCatcher.check_chat_id(act_msg.peer_id):
            return

        me = await Config.TG_CLIENT.get_me()
        if isinstance(act_msg, types.MessageActionChatAddUser) and me.id in act_msg.action.users:
            await Config.QUEUE_EVENTS.put(HandleEvents.processing_action_add_chat_user(event))

        elif isinstance(act_msg, types.MessageActionChatDeleteUser) and me.id in act_msg.action.users:
            await Config.QUEUE_EVENTS.put(HandleEvents.processing_action_chat_delete_user(event))

    @staticmethod
    async def event_raw(event: events.Raw):
        if isinstance(event, types.UpdateNewChannelMessage):
            action = event.message.action
            if not action:
                return

            if isinstance(action, types.MessageActionTopicEdit):
                if await EventsCatcher.check_chat_id(event.message.peer_id):
                    return

                await Config.QUEUE_EVENTS.put(HandleEvents.processing_topic_edited(event))
