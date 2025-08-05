from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="general_")
    host: AnyUrl
