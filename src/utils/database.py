from contextlib import contextmanager
from functools import cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.configurations import get_database_config


@cache
def get_engine():
    db_url = get_database_config().url

    application_name = get_database_config().application_name
    if application_name is not None:
        db_url += f"?application_name={application_name}"

    pool_size = get_database_config().pool_size
    max_overflow = get_database_config().max_overflow

    return create_engine(db_url, pool_size=pool_size, max_overflow=max_overflow)


@contextmanager
def session_manager(autocommit: bool = True):
    engine = get_engine()

    with Session(engine, expire_on_commit=False) as session:
        yield session

        if autocommit:
            session.commit()
