import datetime
from datetime import date, datetime as dt
from random import shuffle

from db.model import Person
from loader import repository


class _Feed:
    _index: int = 0
    _cycle: int = 5
    _user_id: int
    _prev_user_id: int
    _current_user_id: int
    _last_date: date = dt(datetime.MINYEAR, 1, 1)
    _feed_users: [int]

    def __init__(self, user_id):
        self._user_id = user_id
        self._current_user_id = None
        self._prev_user_id = None
        self._last_date = None
        self._feed_users = self._load_feed_users

    @property
    def _load_feed_users(self) -> [int]:
        person_ids = repository.get_feed(repository.get_person(self._user_id))
        if person_ids:
            person = repository.get_person(person_ids[0])
            self._last_date = person.registration_date
        return shuffle(person_ids)

    @property
    def _new_feed_users(self) -> [int]:
        return shuffle(repository.get_feed(repository.get_person(self._user_id), self._last_date))

    @property
    def user_id(self):
        return self._user_id

    @property
    def prev_id(self):
        return self._prev_user_id

    @property
    def current_id(self):
        return self._current_user_id

    @property
    def feed(self):
        return self._feed_users

    @property
    def next(self) -> Person | None:
        self._index = (self._index + 1) % self._cycle
        if not self._index:
            self._feed_users += self._new_feed_users
        try:
            if not self._feed_users:
                self._feed_users = self._load_feed_users
            person = repository.get_person(self._feed_users.pop())
            if not person:
                return self.next
            self._prev_user_id, self._current_user_id = self._current_user_id, person.user_id
            return person
        except IndexError:
            self._prev_user_id, self._current_user_id = self._current_user_id, None
            return None


class Feed:
    _feeds: dict[int, _Feed] = dict()

    def __new__(cls, user_id) -> _Feed:
        if user_id not in cls._feeds:
            cls._feeds[user_id] = _Feed(user_id=user_id)
        return cls._feeds[user_id]
