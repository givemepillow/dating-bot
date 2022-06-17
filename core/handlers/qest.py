from datetime import date

from aiogram import types
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.emoji import emojize

from core import Questionnaire, Feed
from core.markups.inline import *
from core.markups.text import *
from core.services import MessageBox
from core.states import QState, FState
from core.tools import age_suffix, Filter
from loader import dp, bot
from .templates import send_quest_if_person


@dp.message_handler(commands=['cancel'], state=QState.states)
async def cancel(message: Message):
    text = "Ну вот... всё потеряно... Попробовать ещё раз?"
    _user_id = message.from_user.id
    await MessageBox.delete_last(_user_id)
    await QState.first()
    await message.answer(text=text, reply_markup=yesno_keyboard)


@dp.message_handler(text=['Назад'], state=QState.input_name)
@dp.message_handler(commands=['start'], state='*')
async def welcome(message: Message):
    text = "Добро пожаловать! Ну что, начнём?"
    await QState.start.set()
    await message.answer(text=text, reply_markup=welcome_keyboard)


@dp.message_handler(text=['Нет'], state=QState.start)
async def start(message: Message):
    await message.answer("Ладно... Если передумаешь, то просто напиши - /start", reply_markup=ReplyKeyboardRemove())
    await QState.first()  # Update state.


@dp.message_handler(text=['Назад'], state=QState.select_gender)
@dp.message_handler(text=['Начнём', 'Да'], state=[QState.start, QState.complete])
async def start(message: Message):
    await message.answer("Давай знакомиться, как тебя зовут: ", reply_markup=back_keyboard)
    await QState.input_name.set()  # Update state.


@dp.message_handler(state=QState.input_name)
async def name(message: Message):
    _name = ' '.join(map(str.capitalize, message.text.split()))
    if not (20 > len(_name) > 1):
        await message.answer("Длина имени должна быть от 2 до 20 символов.")
        await message.answer("Введите ваше имя:")
    elif not all(char.isalpha() or char == ' ' for char in _name):
        await message.answer("Имя может содержать только буквы.")
        await message.answer("Введите ваше имя:")
    else:
        _user_id = message.from_user.id
        Questionnaire.write(user_id=_user_id, name=_name)
        Questionnaire.write(user_id=_user_id, enabled=True)
        Questionnaire.write(user_id=_user_id, username=message.from_user.username)
        _message = await message.answer(
            f"Приятно познакомиться, {_name}! Выбери свой пол:",
            reply_markup=GenderSelector.markup()
        )
        MessageBox.put(user_id=message.from_user.id, message=_message)
        await QState.select_gender.set()  # Update state.


@dp.callback_query_handler(state=QState.select_gender)
async def gender(callback_query: CallbackQuery):
    _user_id = callback_query.from_user.id
    await MessageBox.delete_last(user_id=_user_id)
    if callback_query.data != 'back':
        Questionnaire.write(user_id=_user_id, gender=callback_query.data)
        _message = await callback_query.message.answer("А кого хочешь найти?", reply_markup=LookingForSelector.markup())
        MessageBox.put(user_id=_user_id, message=_message)
        await QState.select_looking_for.set()  # Update state.
    else:
        _message = await callback_query.message.answer("Как тебя зовут?")
        await QState.previous()  # Update state.


@dp.callback_query_handler(state=QState.select_looking_for)
async def looking_for(callback_query: CallbackQuery):
    _user_id = callback_query.from_user.id
    await MessageBox.delete_last(user_id=_user_id)
    if callback_query.data != 'back':
        _looking_for = None if callback_query.data not in ('male', 'female') else callback_query.data
        Questionnaire.write(user_id=_user_id, looking_for=_looking_for)
        await callback_query.message.answer(f"Принято, {Questionnaire.get(_user_id, 'name')}! Напиши откуда ты: ")
        await QState.search_settlement.set()  # Update state.
    else:
        _message = await callback_query.message.answer(
            "Выбери свой пол:",
            reply_markup=GenderSelector.markup()
        )
        MessageBox.put(user_id=_user_id, message=_message)
        await QState.previous()  # Update state.


@dp.message_handler(state=QState.search_settlement)
async def search(message):
    await types.ChatActions.typing()
    await QState.select_settlement.set()

    _user_id = message.from_user.id

    settlements = Questionnaire.search_settlements(name=message)

    SettlementSelector.setup(settlements=settlements, user_id=_user_id)

    _text1 = emojize(f":mag_right: <i>Результаты по запросу</i> <b>«{message.text}» </b> ")
    _text2 = emojize(f":mag_right: <i>По запросу</i> <b>«{message.text}»</b> <i>ничего не найдено</i> :( ")

    _message = await message.answer(
        text=_text1 if len(settlements) else _text2,
        reply_markup=SettlementSelector.markup(user_id=_user_id),
        parse_mode="HTML"
    )

    MessageBox.put(message=_message, user_id=_user_id)


@dp.callback_query_handler(
    SettlementSelector.data.filter(action=[SettlementSelector.actions.next, SettlementSelector.actions.prev]),
    state=QState.select_settlement.state
)
async def select_process(callback_query, callback_data):
    _user_id = callback_query.from_user.id
    _message = await callback_query.message.edit_reply_markup(
        reply_markup=SettlementSelector.markup(
            user_id=_user_id, callback_data=callback_data
        )
    )
    MessageBox.put(message=_message, user_id=_user_id)


@dp.callback_query_handler(
    SettlementSelector.data.filter(action=SettlementSelector.actions.back),
    state=QState.select_settlement.state
)
async def back(callback_query):
    _user_id = callback_query.from_user.id
    SettlementSelector.clear(_user_id)
    await MessageBox.delete_last(_user_id)
    await callback_query.message.answer("Напиши из какого ты города:")
    await QState.search_settlement.set()  # Update state.


@dp.callback_query_handler(
    SettlementSelector.data.filter(action=SettlementSelector.actions.select),
    state=QState.select_settlement.state
)
async def done(callback_query, callback_data):
    _user_id = callback_query.from_user.id
    Questionnaire.write(user_id=_user_id, settlement_id=int(callback_data['settlement_id']))
    SettlementSelector.clear(_user_id)
    await MessageBox.delete_last(_user_id)
    DateSelector.setup(user_id=_user_id)
    _message = await callback_query.message.answer(
        "Теперь выбери дату рождения: ",
        reply_markup=DateSelector.markup(_user_id)
    )
    MessageBox.put(message=_message, user_id=_user_id)
    await QState.select_date.set()  # Update state.


@dp.callback_query_handler(
    DateSelector.data.filter(action=[
        DateSelector.actions.next_month, DateSelector.actions.prev_month,
        DateSelector.actions.next_year, DateSelector.actions.next_5_year,
        DateSelector.actions.prev_year, DateSelector.actions.prev_5_year,
        DateSelector.actions.select_day
    ]),
    state=QState.select_date.state
)
async def calendar_selection(callback_query: CallbackQuery, callback_data: dict):
    _user_id = callback_query.from_user.id
    if _user_id in DateSelector.users():
        _message = await callback_query.message.edit_reply_markup(
            DateSelector.markup(
                user_id=_user_id,
                callback_data=callback_data
            )
        )
        MessageBox.put(message=_message, user_id=_user_id)
    else:
        await callback_query.answer()


@dp.callback_query_handler(
    DateSelector.data.filter(action=DateSelector.actions.confirm),
    state=QState.select_date.state
)
async def calendar_selection(callback_query: CallbackQuery, callback_data: dict):
    _user_id = callback_query.from_user.id
    await MessageBox.delete_last(user_id=_user_id)
    DateSelector.clear(user_id=_user_id)
    _date_of_birth = date(
        day=int(callback_data['day']),
        month=int(callback_data['month']),
        year=int(callback_data['year'])
    )
    Questionnaire.write(user_id=_user_id, date_of_birth=_date_of_birth)
    _age, _suffix = age_suffix(_date_of_birth)
    await callback_query.message.answer(f'Отлично тебе {_age} {_suffix}.')
    await callback_query.message.answer(f'Пришли нам свою фотографию:')
    await QState.get_photo.set()  # Update state.


@dp.message_handler(content_types=['photo'], state=QState.get_photo)
async def get_photo(message: Message):
    _user_id = message.from_user.id
    _photo = message.photo[-1].file_id
    Questionnaire.write(user_id=_user_id, photo=_photo)
    await message.answer(f"Отлично смотришься, {Questionnaire.get(_user_id, 'name')}.")
    await message.answer(text='Введите свой рост:')
    await QState.select_height.set()  # Update state.


@dp.message_handler(state=QState.select_height)
async def height_selection(message: Message):
    _user_id = message.from_user.id
    _height = message.text
    if not _height.isdigit():
        await message.answer(text='У нас рост измеряется в целых положительных числах!')
        await message.answer(text='Введите свой рост:')
    elif not 0 < int(_height) < 300:
        await message.answer(text='Введите свой настоящий рост')
    else:
        HeightSelector.setup(message.from_user.id)
        _message = await message.answer(text=emojize(':straight_ruler: А теперь выбери предпочтительный рост партнёра'),
                                        reply_markup=HeightSelector.markup(message.from_user.id))
        MessageBox.put(user_id=_user_id, message=_message)
        await QState.select_partner_height.set()  # Update state.
    Questionnaire.write(user_id=_user_id, height=_height)


@dp.callback_query_handler(HeightSelector.data.filter(), state=QState.select_partner_height)
async def height_cd(callback_query, callback_data):
    _user_id = callback_query.from_user.id
    if callback_data['action'] == 'check_mark':
        Questionnaire.write(user_id=_user_id, from_height=HeightSelector.from_height(_user_id))
        Questionnaire.write(user_id=_user_id, to_height=HeightSelector.to_height(_user_id))
        await MessageBox.delete_last(user_id=_user_id)
        HeightSelector.clear(user_id=_user_id)
        await QState.bio.set()
        await callback_query.message.answer(
            text='Напиши что-нибудь о себе, но не забывай, что краткость - сестра таланта!'
        )
    else:
        _message = await callback_query.message.edit_reply_markup(
            HeightSelector.markup(callback_query.from_user.id, callback_data))
        MessageBox.put(message=_message, user_id=_user_id)


@dp.message_handler(state=QState.bio)
async def bio(message: Message):
    _user_id = message.from_user.id
    _bio = message.text.lower()
    _bad_word = Filter.check(_bio)
    if len(_bio) > 500:
        await message.answer(text='Весьма занимательно, попробуйте написать о себе в более сжатом виде :)')
    elif _bad_word is not None:
        await message.answer(
            text=f'Ваше описание содержит нецензурную лексику: "{_bad_word}". Давайте обойдёмся без нехороших слов :)')
    else:
        Questionnaire.write(user_id=_user_id, bio=_bio)
        person = Questionnaire.create_user(_user_id)
        await message.answer(text=f"Отлично!\n"
                                  f"Вот твоя анкета:")
        _age, _suffix = age_suffix(person.date_of_birth)
        await bot.send_photo(photo=person.photo, chat_id=_user_id,
                             caption=f"{person.name}, {person.settlement.name} - {_age} {_suffix}\n"
                                     f"\n {person.bio}")
        await message.answer(text="Хочешь поменять что-то?",
                             reply_markup=after_complete_keyboard)
        await QState.complete.set()


@dp.message_handler(text=['Нет, приступить к поиску', 'Нет'], state=QState.complete)
@dp.message_handler(text=['Смотреть анкеты'], state=FState.sleeping)
@dp.message_handler()
async def complete(message: Message):
    _user_id = message.from_user.id
    await message.answer(text='Приступаем к поиску анкет!', reply_markup=rate_keyboard)
    await FState.looking.set()
    person = Feed(_user_id).next
    await send_quest_if_person(_user_id, person)
    # if person:
    #     await send_quest(_user_id, person)
    # else:
    #     await bot.send_message(text='Подходящих анкет больше нет...', chat_id=_user_id)
