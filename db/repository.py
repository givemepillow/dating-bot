from datetime import datetime as dt
import datetime

from sqlalchemy import desc, select, update
from sqlalchemy.sql.elements import or_, and_
from sqlalchemy.sql.operators import ilike_op

from utils import Singleton
from db.model import Person, Settlement


class Repository(Singleton):
    def __init__(self, session):
        self._session = session

    def add_person(self, person: Person):
        with self._session() as s:
            result = s.execute(select(Person).where(Person.user_id == person.user_id))
            if result.one_or_none() is None:
                s.add(person)
            else:
                s.execute((
                    update(Person).
                    where(Person.user_id == person.user_id).
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
            results = s.execute(select(Person).where(Person.user_id == user_id))
            result = results.one_or_none()
            return result[0] if result else result

    def get_settlement(self, settlement_id):
        with self._session() as s:
            results = s.execute(select(Settlement).where(Settlement.id == settlement_id))
            result = results.one_or_none()
            return result[0] if result else result

    def get_settlements(self, name, limit=25) -> list[Settlement]:
        with self._session() as s:
            return s.query(Settlement).where(
                or_(
                    ilike_op(Settlement.name, f'{name.text}%'),
                    ilike_op(Settlement.name, f'%-{name.text}%'),
                    ilike_op(Settlement.name, f'% {name.text}%')
                )
            ).order_by(desc(Settlement.population)).limit(limit).all()

    def get_feed(self, person: Person, after_date: dt = dt(datetime.MINYEAR, 1, 1)) -> int:
        stmt = select(Person.user_id).where(
            and_(
                Person.settlement_id == person.settlement_id,
                Person.user_id != person.user_id,
                Person.registration_date > after_date
            )
        ).where(or_(
            and_(
                Person.gender == person.looking_for,
                Person.looking_for == person.gender
            ), and_(
                Person.looking_for is None,
                or_(
                    person.looking_for is None,
                    person.gender == Person.looking_for
                )
            )
        )).where(
            or_(
                and_(
                    person.gender == 'female',
                    -2 <= (Person.date_of_birth - person.date_of_birth) / 365.25,
                    (Person.date_of_birth - person.date_of_birth) / 365.25 <= 4
                ),
                and_(
                    person.gender == 'male',
                    -4 <= (Person.date_of_birth - person.date_of_birth) / 365.25,
                    (Person.date_of_birth - person.date_of_birth) / 365.25 <= 2
                )
            )
        ).order_by(desc(Person.registration_date))
        with self._session() as s:
            results = s.execute(stmt)
            return [user_id for user_id, in results.all()]
