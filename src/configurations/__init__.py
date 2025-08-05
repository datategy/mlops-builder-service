from functools import cache

from pydantic import TypeAdapter

from .build_agent import BuildAgentConfig
from .database import DBConfig
from .general import GeneralConfig
from .storage import StorageConfig


@cache
def get_general_config() -> GeneralConfig:
    return GeneralConfig.model_validate({})


@cache
def get_database_config() -> DBConfig:
    return TypeAdapter(DBConfig).validate_python({})


@cache
def get_build_agent_config() -> BuildAgentConfig:
    return BuildAgentConfig.model_validate({})


@cache
def get_storage_config() -> StorageConfig:
    return StorageConfig.model_validate({})
