from aiogram.dispatcher.filters.state import StatesGroup, State


class QState(StatesGroup):
    zero = State()
    start = State()
    input_name = State()
    select_gender = State()
    select_looking_for = State()
    search_settlement = State()
    select_settlement = State()
    select_date = State()
    get_photo = State()
    select_height = State()
    select_partner_height = State()
    bio = State()
    complete = State()


class FState(StatesGroup):
    looking = State()
    reporting = State()
    messaging = State()
    sleeping = State()
