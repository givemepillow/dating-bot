from datetime import date

from db.model import Person
from loader import repository


class _Feed:
    _user_id: int
    _prev_user_id: int
    _current_user_id: int
    _last_date: date
    _feed_users: [int]

    def __init__(self, user_id):
        self._user_id = user_id
        self._load_feed_users(user_id)

    def _load_feed_users(self, user_id):
        self._feed_users = repository.get_feed(repository.get_person(user_id))

    def _update_feed_users(self):
        if self._feed_users:
            self._feed_users += repository.get_feed(repository.get_person(self._user_id), self._last_date)
        else:
            self._load_feed_users(self._user_id)

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
        try:
            if not len(self._feed_users):
                self._load_feed_users(self._user_id)
            result = repository.get_person(self._feed_users.pop())
            if not result:
                self._update_feed_users()
                result = repository.get_person(self._feed_users.pop())
            return result
        except IndexError:
            return None


class Feed:
    _feeds: dict[int, _Feed] = dict()

    def __new__(cls, user_id) -> _Feed:
        if user_id not in cls._feeds:
            cls._feeds[user_id] = _Feed(user_id=user_id)
        return cls._feeds[user_id]
