from aiogram.types import ReplyKeyboardMarkup

from .buttons import (
    back_button,
    no_button,
    go_button,
    yes_button,
    cancel_button
)

back_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=1
).add(back_button)

welcome_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
).add(go_button, no_button)

yesno_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
).add(yes_button, no_button)

restart_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
).add(yes_button, no_button)

cancel_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=1
).add(cancel_button)
