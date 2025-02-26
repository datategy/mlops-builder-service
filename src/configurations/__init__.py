from functools import cache

from pydantic import TypeAdapter

from .database import DBConfig
from .general import GeneralConfig


@cache
def get_database_config() -> DBConfig:
    return TypeAdapter(DBConfig).validate_python({})


@cache
def get_general_config() -> GeneralConfig:
    return TypeAdapter(GeneralConfig).validate_python({})
