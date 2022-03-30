from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import loguru
from aiogram.utils.emoji import emojize

class _Actions:
    up_from = 'up_from'
    down_from = 'down_from'
    up_to = 'up_to'
    down_to = 'down_to'
    check_mark = 'check_mark'

class _HeightSelector:
    _start = 0 
    _end = 300

    def __init__(self, callback_data: CallbackData):
        self._data = callback_data

    def build_markup(self, callback_data):
        self._callback_data_handler(callback_data)
        markup = InlineKeyboardMarkup(row_width=4)
        markup.add(
            InlineKeyboardButton(text = 'От', callback_data='_'),
            InlineKeyboardButton(text = 'До', callback_data='_')
            )
        markup.add(
            InlineKeyboardButton(text = 'неважно' if self._start == 0 else self._start, callback_data='_'),
            InlineKeyboardButton(text = 'неважно' if self._end == 300 else self._end, callback_data='_')
        )
        markup.add(
            InlineKeyboardButton(text = emojize(':arrow_down:'), callback_data='_' if self._start == 0 else self._data.new(_Actions.down_from)),
            InlineKeyboardButton(text = emojize(':arrow_up:'), callback_data=self._data.new(_Actions.up_from)),
            InlineKeyboardButton(text = emojize(':arrow_down:'), callback_data=self._data.new(_Actions.down_to)),
            InlineKeyboardButton(text = emojize(':arrow_up:'), callback_data='_' if self._end == 300 else self._data.new(_Actions.up_to)),
            InlineKeyboardButton(text=emojize('Подтвердить :white_check_mark:'), callback_data=self._data.new(_Actions.check_mark))
        )
        return markup

    def _callback_data_handler(self, callback_data):
        match callback_data['action'] if callback_data else None:
            case _Actions.up_from if self._start == 0:
                self._start = 150
            case _Actions.up_from:
                self._start += 5
            case _Actions.down_from:
                self._start = self._start - 5 if self._start > 150 else 0
            case _Actions.up_to:
                self._end = self._end + 5 if self._end < 200 else 300
            case _Actions.down_to if self._end == 300:
                self._end = 200
            case _Actions.down_to:
                self._end -= 5

class HeightSelector:
    _storage: dict[str, _HeightSelector] = dict()
    data = CallbackData('height', 'action')
    actions = _Actions()

    @classmethod
    def setup(cls, user_id):
        cls._storage[user_id] = _HeightSelector(callback_data=cls.data)
    @classmethod
    def markup(cls, user_id, callback_data=None):
        return cls._storage[user_id].build_markup(callback_data=callback_data)
    @classmethod
    def clear(cls, user_id):
        try:
            del cls._storage[user_id]
        except KeyError as err:
            loguru.logger.warning(str(err))
    @classmethod
    def from_height(cls):
        return _HeightSelector._start

    @classmethod
    def to_height(cls):
        return _HeightSelector._end