import abc

from sqlalchemy import text, desc
from sqlalchemy.sql.elements import or_

from utils import SingletonABC
import model


class AbstractRepository(SingletonABC):
    @abc.abstractmethod
    def add_person(self, person: model.Person):
        raise NotImplementedError

    @abc.abstractmethod
    def get_person(self, user_id) -> model.Person:
        raise NotImplementedError

    @abc.abstractmethod
    def get_settlements(self, name) -> [model.Settlement]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add_person(self, person):
        self.session.add(person)

    def get_person(self, user_id):
        return self.session.query(model.Person).filter_by(id=user_id).one()

    def get_settlements(self, name, limit=25) -> [model.Settlement]:
        return self.session.query(model.Settlement).where(
            or_(
                text(f"name ilike '{name.text}%' "),
                text(f"name ilike '%-{name.text}%' "),
                text(f"name ilike '% {name.text}%' "),
            )
        ).order_by(desc(model.Settlement.population)).limit(limit).all()
