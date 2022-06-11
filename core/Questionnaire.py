import inspect
from types import SimpleNamespace

from loader import repository
from db.model import Person, Settlement


class Questionnaire:
    _storage = {int: {}}

    @classmethod
    def get(cls, user_id, value):
        return cls._storage[user_id][value]

    @classmethod
    def write(cls, user_id, **kwargs):
        if user_id not in cls._storage:
            cls._storage[user_id] = {'user_id': user_id}
        cls._storage[user_id] |= kwargs

    @classmethod
    def search_settlements(cls, name) -> list[Settlement]:
        return repository.get_settlements(name=name, limit=25)

    @classmethod
    def create_user(cls, user_id):
        repository.add_person(Person(**cls._storage[user_id]))
        return repository.get_person(user_id=user_id)
