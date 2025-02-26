from pathlib import Path

from sqlalchemy.orm import DeclarativeBase

from ._types import SQLPath


class Base(DeclarativeBase):
    type_annotation_map = {Path: SQLPath}
