from dataclasses import dataclass

import loguru
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from emoji.core import emojize

from model import Settlement

__all__ = ['SettlementSelector']


@dataclass(frozen=True)
class _Actions:
    prev = 'prev'
    next = 'next'
    back = 'back'
    select = 'select'


class _SettlementSelector:
    def __init__(self, settlements: [Settlement], count: int, callback_data: CallbackData):
        self.__count: int = count
        self.__end: int = count
        self.__start: int = 0
        self.__settlements: [Settlement] = settlements
        self._data = callback_data

    def build_markup(self, callback_data):
        markup = InlineKeyboardMarkup(row_width=2)
        if callback_data is not None:
            match callback_data['action']:
                case _Actions.next:
                    self._next()
                case _Actions.prev:
                    self._prev()
        for s in self.__settlements[self.__start:self.__end]:
            _text = s.name if s.name == s.region else s.name + ', ' + s.region
            markup.add(InlineKeyboardButton(text=_text, callback_data=self._data.new(_Actions.select, s.id)))
        if len(self.__settlements) > self.__count:
            markup.add(
                InlineKeyboardButton(
                    text=emojize(':arrow_left:', use_aliases=True),
                    callback_data=self._data.new(_Actions.prev, 0)
                ),
                InlineKeyboardButton(
                    text=emojize(':arrow_right:', use_aliases=True),
                    callback_data=self._data.new(_Actions.next, 0)
                )
            )
        markup.add(InlineKeyboardButton(text=emojize('Назад :leftwards_arrow_with_hook:', use_aliases=True),
                                        callback_data=self._data.new(_Actions.back, 0)))
        return markup

    def _next(self):
        if self.__start >= len(self.__settlements) - self.__count:
            self.__end = self.__count
            self.__start = 0
        else:
            self.__start += self.__count
            self.__end += self.__count

    def _prev(self):
        if self.__start == 0:
            _start = (len(self.__settlements) // self.__count) * self.__count
            self.__start = _start if _start != len(self.__settlements) else _start - self.__count
            self.__end = self.__start + self.__count
        else:
            self.__start -= self.__count
            self.__end -= self.__count


class SettlementSelector:
    _storage: {str: _SettlementSelector} = dict()
    data = CallbackData('settlements', 'action', 'settlement_id')
    actions = _Actions()

    @classmethod
    def setup(cls, settlements: [Settlement], user_id: int, count: int = 5):
        cls._storage[user_id] = _SettlementSelector(
            settlements=settlements,
            count=count,
            callback_data=cls.data
        )

    @classmethod
    def clear(cls, user_id):
        try:
            del cls._storage[user_id]
        except KeyError as err:
            loguru.logger.warning(str(err))

    @classmethod
    def markup(cls, user_id, callback_data=None):
        return cls._storage[user_id].build_markup(callback_data)
