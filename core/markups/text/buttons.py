from aiogram.types import KeyboardButton
from aiogram.utils.emoji import emojize

back_button = KeyboardButton('Назад')
go_button = KeyboardButton('Начнём')
no_button = KeyboardButton('Нет')
yes_button = KeyboardButton('Да')
cancel_button = KeyboardButton('Отмена')

like_button = KeyboardButton(emojize(':heart:'))
write_button = KeyboardButton(emojize(':love_letter:'))
dislike_button = KeyboardButton(emojize(':thumbsdown:'))
sleep_button = KeyboardButton(emojize(':zzz:'))

no_look_button = KeyboardButton('Нет, приступить к поиску')

look_button = KeyboardButton('Смотреть анкеты')
me_button = KeyboardButton('Моя анкета')
leave_button = KeyboardButton('Я больше не хочу никого искать')

return_to_looking_button = KeyboardButton('Вернуться к поиску')
recreate_quest_button = KeyboardButton('Создать анкету заново')
