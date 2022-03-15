from sqlalchemy import (
    Integer,
    String,
    Column,
    Index,
    UniqueConstraint,
    func,
    Table
)

from .metadata import metadata

settlements_table = Table(
    'settlements',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100), nullable=False),
    Column('region', String(100), nullable=False),
    Column('population', Integer, nullable=False),

    UniqueConstraint('name', 'region'),
    Index('settlement_name_index', 'name'),
    Index('settlement_population_index', 'population'),
    Index('settlement_case_insensitive_name_index', func.lower('name')),
)
