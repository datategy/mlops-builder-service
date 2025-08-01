from pathlib import Path

from sqlalchemy.orm import DeclarativeBase

from ._types import SQLPath


class Base(DeclarativeBase):
    type_annotation_map = {Path: SQLPath}


def create_db():
    """Create the database tables."""
    from src.utils.database import get_engine

    engine = get_engine()
    Base.metadata.create_all(engine)
