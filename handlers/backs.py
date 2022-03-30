from aiogram.types import Message

from core import Questionnaire
from loader import dp
from markups.inline import GenderSelector, LookingForSelector, DateSelector
from markups.text import *
from states import QState
from toolkit import MessageBox


@dp.message_handler(text=['Назад'], state=QState.select_looking_for)
async def to_select_gender(message: Message):
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    _name = Questionnaire.get(user_id=_user_id, value='name')
    _message = await message.answer(
        f"Приятно познакомиться, {_name}! Выбери свой пол:",
        reply_markup=GenderSelector.markup()
    )
    MessageBox.put(user_id=message.from_user.id, message=_message)
    await QState.select_gender.set()  # Update state.


@dp.message_handler(text=['Назад'], state=QState.search_settlement)
async def to_select_looking_for(message: Message):
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    await QState.select_gender.set()  # Update state.
    _message = await message.answer("А кого хочешь найти?", reply_markup=LookingForSelector.markup())
    MessageBox.put(user_id=_user_id, message=_message)
    await QState.select_looking_for.set()  # Update state.


@dp.message_handler(text=['Назад'], state=[QState.select_settlement, QState.select_date])
async def to_search(message: Message):
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    await message.answer(f"Напиши откуда ты: ")
    await QState.search_settlement.set()  # Update state.


@dp.message_handler(text=['Назад'], state=QState.get_photo)
async def to_select_date(message: Message):
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    DateSelector.setup(user_id=_user_id)
    _message = await message.answer(
        "Теперь выбери дату рождения: ",
        reply_markup=DateSelector.markup(_user_id)
    )
    MessageBox.put(message=_message, user_id=_user_id)
    await QState.select_date.set()  # Update state.
