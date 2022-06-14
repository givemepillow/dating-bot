from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Date, Index, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Gender(Base):
    __tablename__ = "genders"
    name = Column(String(30), primary_key=True)


class Settlement(Base):
    __tablename__ = "settlements"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(100), nullable=False)
    region = Column('region', String(100), nullable=False)
    population = Column('population', Integer, nullable=False)

    persons = relationship("Person", back_populates="settlement", lazy='subquery')

    __table_args__ = (
        Index('settlement_name_index', 'name'),
        Index('settlement_population_index', 'population'),
        Index('settlement_case_insensitive_name_index', func.lower('name')),
    )


class Person(Base):
    __tablename__ = "persons"
    user_id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String(25), nullable=False)
    photo = Column('photo', String(100), nullable=False)
    registration_date = Column('registration_date', DateTime, default=datetime.now)
    height = Column('height', Integer, nullable=True)
    enabled = Column('enabled', Boolean, nullable=False, default=True)
    bio = Column('bio', String(300), nullable=True)
    settlement_id = Column('settlement_id', Integer, ForeignKey('settlements.id'), nullable=False)
    gender = Column('gender', String(25), ForeignKey('genders.name'), nullable=False)
    from_height = Column('from_height', Integer, nullable=True)
    to_height = Column('to_height', Integer, nullable=True)
    date_of_birth = Column('date_of_birth', Date, nullable=False)
    looking_for = Column('looking_for', String(25), ForeignKey('genders.name'), nullable=True)

    settlement = relationship("Settlement", back_populates="persons", lazy='subquery')

    __table_args__ = (
        Index('person_settlement_id_index', 'settlement_id'),
        Index('person_date_of_birth_index', 'date_of_birth'),
        Index('person_height_for_index', 'height')
    )
