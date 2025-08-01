from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class BaseDBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_", arbitrary_types_allowed=True)

    application_name: str | None = None
    """
    Shown in the postgres `pg_stat_activity` table. It is useful to identify from
    postgres the source of the connections.
    """
    pool_size: int = 1
    """
    Number of connection to keep open with the DB. This is the largest number
    of connections that will be kept persistently in the pool.
    """
    max_overflow: int = 1
    """
    The maximum overflow size of the pool. When the number of checked-out
    connections reaches the size set in pool_size, additional connections will
    be returned up to this limit. When those additional connections are
    returned to the pool, they are disconnected and discarded. It follows then
    that the total number of simultaneous connections the pool will allow is
    pool_size + max_overflow, and the total number of “sleeping” connections the
    pool will allow is pool_size.
    """


class ManualDBCredConfig(BaseDBConfig):
    host: str
    name: str
    username: str
    password: SecretStr
    port: int
    dialect: str

    @property
    def url(self) -> str:
        protocol = f"{self.dialect}"
        credentials = f"{self.username}:{self.password.get_secret_value()}"
        address = f"{self.host}:{self.port}/{self.name}"
        return f"{protocol}://{credentials}@{address}"


class URLDBCredConfig(BaseDBConfig):
    url: URL


type DBConfig = ManualDBCredConfig | URLDBCredConfig
