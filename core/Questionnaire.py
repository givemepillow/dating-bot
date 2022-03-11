import inspect

from loader import repository
from model import Person, Settlement


class Questionnaire:
    _storage = {int: {}}

    @classmethod
    def get(cls, user_id, value):
        return cls._storage[user_id][value]

    @classmethod
    def write(cls, user_id, **kwargs):
        args = set(kwargs)
        awaited_args = set(inspect.getfullargspec(Person.__init__).args)
        if not args <= awaited_args:
            raise KeyError(f"Incorrect parameters: {', '.join(args - awaited_args)}.")
        if user_id not in cls._storage:
            cls._storage[user_id] = {'user_id': user_id}
        cls._storage[user_id] |= kwargs

    @classmethod
    def search_settlements(cls, name) -> [Settlement]:
        return repository.get_settlements(name=name, limit=25)

    @classmethod
    def create_user(cls, user_id):
        # person = Person(**cls._storage[user_id])
        # repository.add_person(person)
        ...
