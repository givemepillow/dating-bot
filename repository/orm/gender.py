from sqlalchemy import Table, Column, Integer, String

from .metadata import metadata

genders_table = Table(
    'genders',  # name: str
    metadata,  # metadata: MetaData
    Column('name', String(25), primary_key=True, nullable=False)
)
