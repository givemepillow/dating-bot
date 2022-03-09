from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji.core import emojize


class GenderSelector:
    @staticmethod
    def markup():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text=emojize('Я девушка :woman:', use_aliases=True),
                                 callback_data='female'),
            InlineKeyboardButton(text=emojize('Я парень :man:', use_aliases=True),
                                 callback_data='male'),
            InlineKeyboardButton(text=emojize('Назад :leftwards_arrow_with_hook:', use_aliases=True),
                                 callback_data='back')
        )
