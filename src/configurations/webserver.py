from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornConfig(BaseSettings):
    """
    Configuration for the Uvicorn web server.
    """

    model_config = SettingsConfigDict(env_prefix="uvicorn_")

    host: str = "0.0.0.0"
    port: int = 2025
