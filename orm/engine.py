import csv

from sqlalchemy import create_engine, insert

from model import Settlement
from .mapper import run_mapper
from .metadata import metadata


def database_engine(
        username='postgres',
        password='',
        host='localhost',
        database='dating',
        echo=True,
        pool_size=6,
        max_overflow=10,
        encoding='utf-8',
        drop=True,
        connect=True,
        create=True,
        data_source=None
):
    db_engine = create_engine(
        f"postgresql+psycopg2://{username}:{password}@{host}/{database}",
        echo=echo, pool_size=pool_size, max_overflow=max_overflow, encoding=encoding
    )

    if connect:
        db_engine.connect()

    run_mapper()

    if drop:
        metadata.drop_all(db_engine)

    if create:
        metadata.create_all(db_engine)
        if data_source:
            with open(data_source, 'r') as f:
                reader = csv.DictReader(f)
                with db_engine.connect() as connection:
                    connection.execute(
                        insert(Settlement),
                        [
                            {'name': row['settlement'], 'region': row['region'], 'population': int(row['population'])}
                            for row in reader
                        ]
                    )

    return db_engine
