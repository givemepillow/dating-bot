from contextlib import suppress

from aiogram.types import Message
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from loader import bot


class MessageBox:
    _storage: {int: []} = dict()

    @classmethod
    def save(cls, message: Message, user_id: int):
        if user_id not in cls._storage:
            cls._storage[user_id] = []
            cls._storage[user_id].append(message)
        else:
            cls._storage[user_id].append(message)

    @classmethod
    def get(cls, user_id: int) -> Message:
        if user_id in cls._storage and cls._storage[user_id]:
            return cls._storage[user_id].pop()
        else:
            return None

    @classmethod
    async def delete_last(cls, user_id: int):
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            _message = cls.get(user_id=user_id)
            if _message is not None:
                await bot.delete_message(chat_id=user_id, message_id=_message.message_id)
