from aiogram.types import ReplyKeyboardMarkup

from .buttons import (
    back_button,
    no_button,
    go_button,
    yes_button,
    cancel_button,
    like_button,
    write_button,
    dislike_button,
    sleep_button,
    no_look_button,
    look_button,
    me_button,
    leave_button
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

rate_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=4
).add(like_button,
      write_button,
      dislike_button,
      sleep_button
      )

after_complete_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
).add(yes_button, no_look_button)

sleeping_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=3
).add(look_button, me_button, leave_button)
