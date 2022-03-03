from contextlib import suppress

from aiogram.types import Message
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from loader import bot


class MessageBox:
    _storage: {int: Message} = dict()

    @classmethod
    def save(cls, message: Message, user_id: int):
        cls._storage[user_id] = message

    @classmethod
    def get(cls, user_id: int) -> Message:
        return cls._storage[user_id]

    @classmethod
    async def delete_last(cls, user_id: int):
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound, KeyError):
            _message = cls.get(user_id=user_id)
            await bot.delete_message(chat_id=user_id, message_id=_message.message_id)
