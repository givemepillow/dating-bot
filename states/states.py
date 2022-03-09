from aiogram.dispatcher.filters.state import StatesGroup, State


class QState(StatesGroup):
    start = State()
    input_name = State()
    search_settlement = State()
    select_settlement = State()
    select_date = State()
    select_gender = State()
    select_looking_for = State()