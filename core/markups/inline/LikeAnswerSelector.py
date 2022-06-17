from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.emoji import emojize


class LikeAnswerSelector:
    @staticmethod
    def markup():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text=emojize(':heart:'),
                                 callback_data='like'),
            InlineKeyboardButton(text=emojize(':thumbsdown:'),
                                 callback_data='dislike')
        )
