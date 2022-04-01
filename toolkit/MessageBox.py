from contextlib import suppress

from aiogram.types import Message
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from loader import bot


class MessageBox:
    _storage: dict[int: [Message]] = dict()
    _messages: dict[int: {int}] = dict()

    @classmethod
    def put(cls, message: Message, user_id: int):
        if user_id not in cls._messages:
            cls._messages[user_id] = set()
        if message.message_id not in cls._messages[user_id]:
            cls._messages[user_id].add(message.message_id)
            if user_id not in cls._storage:
                cls._storage[user_id] = []
            cls._storage[user_id].append(message)

    @classmethod
    def get(cls, user_id: int) -> Message | None:
        if user_id in cls._storage and cls._storage[user_id]:
            return cls._storage[user_id].pop()
        else:
            return None

    @classmethod
    async def delete_last(cls, user_id: int):
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            _message = cls.get(user_id=user_id)
            if _message is not None:
                if user_id in cls._messages:
                    cls._messages[user_id].discard(_message.message_id)
                await bot.delete_message(chat_id=user_id, message_id=_message.message_id)

    @classmethod
    async def replace_last(cls, user_id: int, message: Message):
        """
        Deleting last message at the user's stack and put
        on new message.
        """
        await cls.delete_last(user_id=user_id)
        cls.put(message=message, user_id=user_id)
