from functools import cache

from pydantic import TypeAdapter

from .build_agent import BuildAgentConfig
from .database import DBConfig
from .storage import StorageConfig


@cache
def get_database_config() -> DBConfig:
    return TypeAdapter(DBConfig).validate_python({})


@cache
def get_build_agent_config() -> BuildAgentConfig:
    return TypeAdapter(BuildAgentConfig).validate_python({})


@cache
def get_storage_config() -> StorageConfig:
    return TypeAdapter(StorageConfig).validate_python({})
