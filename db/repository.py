from sqlalchemy import desc, select, update
from sqlalchemy.sql.elements import or_
from sqlalchemy.sql.operators import ilike_op

from utils import Singleton
from db import model


class Repository(Singleton):
    def __init__(self, session):
        self._session = session

    def add_person(self, person: model.Person):
        with self._session() as s:
            result = s.execute(select(model.Person).where(model.Person.user_id == person.user_id))
            if result.one_or_none() is None:
                s.add(person)
            else:
                s.execute((
                    update(model.Person).
                    where(model.Person.user_id == person.user_id).
                    values(
                        name=person.name,
                        photo=person.photo,
                        registration_date=person.registration_date,
                        height=person.height,
                        enabled=person.enabled,
                        bio=person.bio,
                        settlement_id=person.settlement_id,
                        gender=person.gender,
                        from_height=person.from_height,
                        to_height=person.to_height,
                        date_of_birth=person.date_of_birth,
                        looking_for=person.looking_for
                    )
                ))
            s.commit()

    def get_person(self, user_id):
        with self._session() as s:
            results = s.execute(select(model.Person).where(model.Person.user_id == user_id))
            result = results.one_or_none()
            return result[0] if result else result

    def get_settlement(self, settlement_id):
        with self._session() as s:
            results = s.execute(select(model.Settlement).where(model.Settlement.id == settlement_id))
            result = results.one_or_none()
            return result[0] if result else result

    def get_settlements(self, name, limit=25) -> list[model.Settlement]:
        with self._session() as s:
            return s.query(model.Settlement).where(
                or_(
                    ilike_op(model.Settlement.name, f'{name.text}%'),
                    ilike_op(model.Settlement.name, f'%-{name.text}%'),
                    ilike_op(model.Settlement.name, f'% {name.text}%')
                )
            ).order_by(desc(model.Settlement.population)).limit(limit).all()
