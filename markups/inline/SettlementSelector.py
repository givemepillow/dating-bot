from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from model.Settlement import Settlement

__all__ = ['SettlementSelector']


class _SettlementSelector:
    def __init__(self, settlements: [Settlement], count: int):
        self.__count: int = count
        self.__end: int = count
        self.__start: int = 0
        self.__settlements: [Settlement] = settlements

    def build_markup(self, action=None):
        markup = InlineKeyboardMarkup(row_width=2)
        match action:
            case 'next':
                self.__next()
            case 'prev':
                self.__prev()
        for s in self.__settlements[self.__start:self.__end]:
            _text = s.name if s.name == s.region else s.name + ', ' + s.region
            markup.add(InlineKeyboardButton(text=_text, callback_data=s.id))
        if len(self.__settlements) > self.__count:
            markup.add(
                InlineKeyboardButton(text='⬅️', callback_data='prev'),
                InlineKeyboardButton(text='➡️', callback_data='next')
            )
        markup.add(InlineKeyboardButton(text='Назад ↩️', callback_data='back'))
        return markup

    def __next(self):
        if self.__start >= len(self.__settlements) - self.__count:
            self.__end = self.__count
            self.__start = 0
        else:
            self.__start += self.__count
            self.__end += self.__count

    def __prev(self):
        if self.__start == 0:
            _start = (len(self.__settlements) // self.__count) * self.__count
            self.__start = _start if _start != len(self.__settlements) else _start - self.__count
            self.__end = self.__start + self.__count
        else:
            self.__start -= self.__count
            self.__end -= self.__count


class SettlementSelector:
    storage: {str: _SettlementSelector} = dict()

    @classmethod
    def init(cls, settlements: [Settlement], user_id: int, count: int = 5):
        cls.storage[user_id] = _SettlementSelector(settlements=settlements, count=count)

    @classmethod
    def clear(cls, user_id):
        del cls.storage[user_id]

    @classmethod
    def update_markup(cls, user_id, action=None):
        return cls.storage[user_id].build_markup(action)
