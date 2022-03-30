from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


class LookingForSelector:
    @staticmethod
    def markup():
        return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(text=emojize('Девушку :princess:'),
                                 callback_data='female'),
            InlineKeyboardButton(text=emojize('Парня :person_with_blond_hair:'),
                                 callback_data='male'),
            InlineKeyboardButton(text=emojize('Неважно :v:'),
                                 callback_data='no_matter')
        )
