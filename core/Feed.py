import datetime
from datetime import date, datetime as dt
from random import shuffle

from db.model import Person
from loader import repository


class _Feed:
    _index: int = 0
    _cycle: int = 5
    _user_id: int
    _prev_user_id: int | None
    _current_user_id: int | None
    _last_date: date | None = dt(datetime.MINYEAR, 1, 1)
    _feed_users: [int]
    _user_likes: [int]

    def __init__(self, user_id):
        self._user_id = user_id
        self._current_user_id = None
        self._prev_user_id = None
        self._last_date = None
        self._feed_users = self._load_feed_users
        self._user_likes = list()

    @property
    def _load_feed_users(self) -> [int]:
        person_ids = repository.get_feed(repository.get_person(self._user_id))
        if person_ids:
            person = repository.get_person(person_ids[0])
            self._last_date = person.registration_date
        shuffle(person_ids)
        return person_ids

    @property
    def _new_feed_users(self) -> [int]:
        new_users = repository.get_feed(
            repository.get_person(self._user_id),
            self._last_date if self._last_date else dt(datetime.MINYEAR, 1, 1)
        )
        shuffle(new_users)
        return new_users

    def get_like(self) -> int | None:
        if self._user_likes:
            return self._user_likes.pop()
        else:
            return None

    def set_like(self, user_id: int):
        self._user_likes.append(user_id)

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def prev_id(self) -> int | None:
        return self._prev_user_id

    @property
    def current_id(self) -> int | None:
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
