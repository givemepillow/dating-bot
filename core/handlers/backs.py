from aiogram.types import Message
from aiogram.utils.emoji import emojize

from core import Questionnaire
from loader import dp
from core.markups.inline import GenderSelector, LookingForSelector, DateSelector, HeightSelector
from core.states import QState
from core.tools import MessageBox


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


@dp.message_handler(text=['Назад'], state=QState.select_height)
async def to_select_photo(message: Message):
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    await message.answer(f'Пришли нам свою фотографию:')
    await QState.get_photo.set()  # Update state.


@dp.message_handler(text=['Назад'], state=QState.select_partner_height)
async def to_select_height(message: Message):
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    await message.answer(text='Введите свой рост:')
    await QState.select_height.set()  # Update state.


@dp.message_handler(text=['Назад'], state=QState.bio)
async def to_select_height(message: Message):
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    HeightSelector.setup(message.from_user.id)
    await message.answer(text=emojize(':straight_ruler: А теперь выбери предпочтительный рост партнёра'),
                         reply_markup=HeightSelector.markup(message.from_user.id))
    await QState.select_partner_height.set()  # Update state.
