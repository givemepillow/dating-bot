import inspect

from model import Person


class Questionnaire:
    _storage = {int: {}}

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
    def create_user(cls, user_id):
        # person = Person(**cls._storage[user_id])
        # repository.add_person(person)
        ...
