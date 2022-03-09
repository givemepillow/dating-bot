import calendar
from dataclasses import dataclass
from datetime import datetime, timedelta

import loguru
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
from emoji.core import emojize

__all__ = ['DateSelector']


@dataclass(frozen=True)
class _Actions:
    prev_year = 'prev_year'
    next_year = 'next_year'
    prev_5_year = 'prev_5_year'
    next_5_year = 'next_5_year'
    prev_month = 'prev_month'
    next_month = 'next_month'
    prev_3_month = 'prev_3_month'
    next_3_month = 'next_3_month'
    select_day = 'select_day'
    confirm = 'confirm'


class _DateSelector:
    def __init__(self, callback_data, default_year=2002, default_month=1):
        self._data = callback_data
        self._year = default_year
        self._month = default_month
        self._selected_day = 0
        self._selected_month = 0
        self._selected_year = 0

    def build_markup(self, callback_data):
        self._callback_data_handler(callback_data)
        markup = InlineKeyboardMarkup(row_width=7)
        self._build_year(markup)
        self._build_month(markup)
        self._build_weekdays(markup)
        self._build_days(markup)
        self._build_confirm(markup)
        return markup

    def _callback_data_handler(self, callback_data):
        if callback_data is None:
            return
        match callback_data['action']:
            case _Actions.select_day:
                day = int(callback_data['day'])
                year = int(callback_data['year'])
                month = int(callback_data['month'])
                if day == self._selected_day and year == self._selected_year and self._selected_month == month:
                    self._selected_day = 0
                else:
                    self._selected_day, self._selected_year, self._selected_month = day, year, month
            case _Actions.next_year:
                self._year += 1
            case _Actions.prev_year:
                self._year -= 1
            case _Actions.prev_5_year:
                self._year -= 5
            case _Actions.next_5_year:
                self._year += 5
            case _Actions.next_month:
                _date = datetime(self._year, self._month, 1) + timedelta(days=31)
                self._month, self._year = _date.month, _date.year
            case _Actions.prev_month:
                _date = datetime(self._year, self._month, 1) - timedelta(days=1)
                self._month, self._year = _date.month, _date.year
            case _Actions.next_3_month:
                _date = datetime(self._year, self._month, 1) + timedelta(days=31 * 3)
                self._month, self._year = _date.month, _date.year
            case _Actions.prev_3_month:
                _date = datetime(self._year, self._month, 1) - timedelta(days=31 * 2 + 1)
                self._month, self._year = _date.month, _date.year

    def _build_year(self, markup):
        markup.add(
            InlineKeyboardButton(emojize(':rewind:', use_aliases=True), callback_data=self._data.new(
                _Actions.prev_5_year, self._year, self._month, 0
            )),
            InlineKeyboardButton(emojize(':arrow_backward:', use_aliases=True), callback_data=self._data.new(
                _Actions.prev_year, self._year, self._month, 0
            )),

            InlineKeyboardButton(str(self._year), callback_data='_'),

            InlineKeyboardButton(emojize(':arrow_forward:', use_aliases=True), callback_data=self._data.new(
                _Actions.next_year, self._year, self._month, 0
            )),
            InlineKeyboardButton(emojize(':fast_forward:', use_aliases=True), callback_data=self._data.new(
                _Actions.next_5_year, self._year, self._month, 0
            ))
        )
        return markup

    def _build_month(self, markup):
        markup.add(
            InlineKeyboardButton(emojize(':rewind:', use_aliases=True), callback_data=self._data.new(
                _Actions.prev_3_month, self._year, self._month, 0
            )),
            InlineKeyboardButton(emojize(':arrow_backward:', use_aliases=True), callback_data=self._data.new(
                _Actions.prev_month, self._year, self._month, 0
            )),

            InlineKeyboardButton(str(calendar.month_name[self._month]), callback_data='_'),

            InlineKeyboardButton(emojize(':arrow_forward:', use_aliases=True), callback_data=self._data.new(
                _Actions.next_month, self._year, self._month, 0
            )),
            InlineKeyboardButton(emojize(':fast_forward:', use_aliases=True), callback_data=self._data.new(
                _Actions.next_3_month, self._year, self._month, 0
            ))
        )
        return markup

    @staticmethod
    def _build_weekdays(markup):
        markup.add(*(
            InlineKeyboardButton(str(weekday), callback_data='_')
            for weekday in calendar.day_abbr
        ))
        return markup

    def _build_days(self, markup):
        month = calendar.monthcalendar(self._year, self._month)
        for week in month:
            markup.row()
            for day in week:
                if day == 0:
                    markup.insert(InlineKeyboardButton(" ", callback_data='_'))
                else:
                    markup.insert(InlineKeyboardButton(self._mark_day(day), callback_data=self._data.new(
                        _Actions.select_day, self._year, self._month, day
                    )))
        return markup

    def _build_confirm(self, markup):
        if self._selected_day != 0:
            markup.add(InlineKeyboardButton(
                emojize(
                    f':grey_exclamation: '
                    f'Подтвердить {self._selected_day:02d}.{self._selected_month:02d}.{self._selected_year} '
                    f':grey_question:',
                    use_aliases=True
                ),
                callback_data=self._data.new(
                    _Actions.confirm, self._selected_year, self._selected_month, self._selected_day
                )
            ))
        else:
            markup.add(InlineKeyboardButton(" ", callback_data='_'))
        return markup

    def _mark_day(self, day):
        if self._year == self._selected_year and self._month == self._selected_month:
            return day if day != self._selected_day else emojize(':white_check_mark:', use_aliases=True)
        else:
            return day


class DateSelector:
    _storage: {int: _DateSelector} = dict()
    data = CallbackData('calendar', 'action', 'year', 'month', 'day')
    actions = _Actions()

    @classmethod
    def setup(cls, user_id):
        cls._storage[user_id] = _DateSelector(callback_data=cls.data)

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
    def users(cls):
        return cls._storage.keys()
