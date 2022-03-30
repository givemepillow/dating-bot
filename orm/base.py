import csv

from sqlalchemy import create_engine, insert, select, func
from model import Settlement
from .mapper import run_mapper
from .metadata import metadata


def create_database_engine(
        username='postgres',
        password='',
        host='localhost',
        database='dating',
        database_engine='postgres',
        echo=True,
        pool_size=6,
        max_overflow=10,
        encoding='utf-8',
        drop=True,
        connect=True,
        create=True,
        data_source=None
):
    match database_engine:
        case 'postgres':
            db_engine = create_engine(
                f"postgresql+psycopg2://{username}:{password}@{host}/{database}",
                echo=echo, pool_size=pool_size, max_overflow=max_overflow, encoding=encoding
            )
        case 'sqlite' | 'sqlite3' | _:
            _db = f"sqlite:///{database}.db" if '.' not in database_engine else f"sqlite:///{database}"
            db_engine = create_engine(_db, echo=echo, encoding=encoding)

    if connect:
        db_engine.connect()

    run_mapper()

    if drop:
        metadata.drop_all(db_engine)

    if create:
        metadata.create_all(db_engine)
        if data_source:
            with db_engine.connect() as connection:
                if connection.execute(select(func.count()).select_from(Settlement)).fetchone()[0] == 0:
                    with open(data_source, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        connection.execute(
                            insert(Settlement),
                            [
                                {'name': row['settlement'], 'region': row['region'], 'population': int(row['population'])}
                                for row in reader
                            ]
                        )
                
                

    return db_engine
