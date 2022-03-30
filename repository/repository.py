import abc

from sqlalchemy import desc
from sqlalchemy.sql.elements import or_
from sqlalchemy.sql.operators import ilike_op

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
    def get_settlements(self, name) -> list[model.Settlement]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, Session):
        self.session = Session()

    def add_person(self, person):
        with self.session as s:
            s.add(person)

    def get_person(self, user_id):
        return self.session.query(model.Person).filter_by(id=user_id).one()

    def get_settlements(self, name, limit=25) -> list[model.Settlement]:
        with self.session as s:
            return s.query(model.Settlement).where(
                or_(
                    ilike_op(model.Settlement.name, f'{name.text}%'),
                    ilike_op(model.Settlement.name, f'%-{name.text}%'),
                    ilike_op(model.Settlement.name, f'% {name.text}%')
                )
            ).order_by(desc(model.Settlement.population)).limit(limit).all()


class Repository(SqlAlchemyRepository):
    pass
