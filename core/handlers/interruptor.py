from aiogram.types import Message

from core import Feed
from core.markups.text import *
from core.states import FState, QState
from loader import dp, repository
from .templates import send_quest_if_person


@dp.message_handler(text='Я больше не хочу никого искать', state=FState.sleeping)
async def disable(message: Message):
    await message.answer(text='Хорошо, сообщи, когда захочешь вернуться!',
                         reply_markup=disabled_keyboard
                         )
    repository.disable_person(message.from_user.id)
    await QState.zero.set()


@dp.message_handler(text='Вернуться к поиску', state=QState.zero)
async def enable(message: Message):
    _user_id = message.from_user.id
    await message.answer(text='Приступаем к поиску анкет!', reply_markup=rate_keyboard)
    repository.enable_person(_user_id)
    await FState.looking.set()
    person = Feed(_user_id).next
    await send_quest_if_person(_user_id, person)
