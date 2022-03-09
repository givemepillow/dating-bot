from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji.core import emojize


class LookingForSelector:
    @staticmethod
    def markup():
        return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(text=emojize('Девушку :princess:', use_aliases=True),
                                 callback_data='female'),
            InlineKeyboardButton(text=emojize('Парня :person_with_blond_hair:', use_aliases=True),
                                 callback_data='male'),
            InlineKeyboardButton(text=emojize('Неважно :v:', use_aliases=True),
                                 callback_data='no_matter'),
            InlineKeyboardButton(text=emojize('Назад :leftwards_arrow_with_hook:', use_aliases=True),
                                 callback_data='back')
        )
