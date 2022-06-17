from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.emoji import emojize

from core import Feed
from core.markups.text import *
from core.services import MessageBox
from core.states import FState, QState
from loader import dp, bot, config, repository
from .templates import send_quest, send_like, send_quest_if_person


@dp.callback_query_handler(state=FState.states)
async def options(callback_query: CallbackQuery):
    _user_id = callback_query.from_user.id
    if callback_query.data == 'report':
        await bot.send_message(_user_id, 'Опишите жалобу: ')
        await FState.reporting.set()
    if callback_query.data == 'previous':
        prev_person_id = Feed(_user_id).prev_id
        prev_person = repository.get_person(prev_person_id)
        if prev_person:
            await send_quest(_user_id, prev_person, callback_query.data)
        else:
            await bot.send_message(text=emojize('Это первая анкета, предыдущей еще нет:upside_down_face:'),
                                   chat_id=_user_id)

    if callback_query.data == 'like':
        like_person = repository.get_person(Feed(callback_query.from_user.id).get_like())
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'Можешь начинать общаться: @{like_person.username}\nНе забудь оценить предыдущую '
                                    f'анкету!')
    if callback_query.data == 'dislike':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text='Ладно... Оцени предыдущую анкету!',
        )
    _message = await callback_query.message.edit_reply_markup(InlineKeyboardMarkup())


@dp.message_handler(state=FState.reporting)
async def report(message: Message):
    _user_id = message.from_user.id
    await bot.send_message(text='Репорт от пользователя '
                                f'{message.from_user.username} (id {_user_id}):\n{message.text}',
                           chat_id=config.bot.admin
                           )
    await message.answer(text='Жалоба отправлена!')
    await FState.looking.set()

    person = Feed(_user_id).next
    await send_quest_if_person(_user_id, person)


@dp.message_handler(text=[emojize(':heart:')], state=FState.looking)
async def looking_like(message: Message):
    _user_id = message.from_user.id
    _prev_message = MessageBox.get(_user_id)
    if _prev_message:
        await _prev_message.edit_reply_markup(InlineKeyboardMarkup())

    await send_like(_user_id)

    next_person = Feed(_user_id).next
    await send_quest_if_person(_user_id, next_person)


@dp.message_handler(text=[emojize(':thumbsdown:')], state=FState.looking)
async def looking_dislike(message: Message):
    _user_id = message.from_user.id
    _prev_message = MessageBox.get(_user_id)
    await _prev_message.edit_reply_markup(InlineKeyboardMarkup())

    person = Feed(_user_id).next
    await send_quest_if_person(_user_id, person)


@dp.message_handler(text=[emojize(':love_letter:')], state=FState.looking)
async def looking_love_letter(message: Message):
    _user_id = message.from_user.id
    _prev_message = MessageBox.get(_user_id)
    await _prev_message.edit_reply_markup(InlineKeyboardMarkup())
    await message.answer(text='Напиши что-то для этого пользователя:')
    await FState.messaging.set()


@dp.message_handler(content_types=['text'], state=FState.messaging)
async def messaging(message: Message):
    _user_id = message.from_user.id
    _message = message.text
    _prev_message = MessageBox.get(_user_id)
    if _prev_message:
        await _prev_message.edit_reply_markup(InlineKeyboardMarkup())
    await message.answer(text='Пользователь получит твое сообщение!')
    await send_like(_user_id, _message)

    await FState.looking.set()
    next_person = Feed(_user_id).next
    await send_quest_if_person(_user_id, next_person)


@dp.message_handler(text=[emojize(':zzz:')], state=FState.looking)
async def go_sleep(message: Message):
    _user_id = message.from_user.id
    _prev_message = MessageBox.get(_user_id)
    await _prev_message.edit_reply_markup(InlineKeyboardMarkup())
    await message.answer(text='Подождем, пока кто-то увидит твою анкету',
                         reply_markup=sleeping_keyboard
                         )
    await FState.sleeping.set()


@dp.message_handler(text='Моя анкета', state=FState.sleeping)
async def me(message: Message):
    _user_id = message.from_user.id
    person = repository.get_person(_user_id)
    await send_quest(_user_id, person, me=True)
    await message.answer(text="Хочешь поменять что-то?",
                         reply_markup=after_complete_keyboard)
    await QState.complete.set()
