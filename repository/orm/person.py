from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Column,
    DateTime,
    Index,
    Boolean,
    Date,
    Table,
    ForeignKey
)

from .metadata import metadata

persons_table = Table(
    'persons',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(25), nullable=False),
    Column('settlement_id', Integer, ForeignKey('settlements.id'), nullable=False),
    Column('registration_date', DateTime, server_default='NOW()', default=datetime.now),
    Column('enabled', Boolean, nullable=False, default=True),
    Column('gender', String(25), ForeignKey('genders.name'), nullable=False),
    Column('date_of_birth', Date, nullable=False),
    Column('looking_for', String(25), ForeignKey('genders.name'), nullable=True),
    Column('bio', String(300), nullable=True),
    Column('photo', String(100), nullable=False),
    Column('height', Integer, nullable=True),
    Column('from_height', Integer, nullable=True),
    Column('to_height', Integer, nullable=True),

    Index('person_settlement_id_index', 'settlement_id'),
    Index('person_date_of_birth_index', 'date_of_birth'),
    Index('person_height_for_index', 'height')
)
