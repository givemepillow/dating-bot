from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


class GenderSelector:
    @staticmethod
    def markup():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text=emojize('Я девушка :woman:'),
                                 callback_data='female'),
            InlineKeyboardButton(text=emojize('Я парень :man:'),
                                 callback_data='male'),
            InlineKeyboardButton(text=emojize('Назад :leftwards_arrow_with_hook:'),
                                 callback_data='back')
        )
