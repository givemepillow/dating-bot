from sqlalchemy import desc
from sqlalchemy.sql.elements import or_
from sqlalchemy.sql.operators import ilike_op

from utils import Singleton
from db import model


class SqlAlchemyRepository(Singleton):
    def __init__(self, Session):
        self.session = Session()

    def add_person(self, person):
        self.session.add(person)
        self.session.commit()

    def get_person(self, user_id):
        return self.session.query(model.Person).filter_by(id=user_id).one()

    def get_settlement(self, settlement_id):
        return self.session.query(model.Settlement).filter_by(id=settlement_id).one()

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
