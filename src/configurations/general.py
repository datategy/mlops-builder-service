from httpx import URL
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.pydantic import AnyHttpxURL


class GeneralConfig(BaseSettings):
    model_config = SettingsConfigDict(arbitrary_types_allowed=True)

    gitlab_private_token: SecretStr = SecretStr("")
    gitlab_project_url: AnyHttpxURL = URL("http://datategy.net")
    """
    URL that points to the project for custom envs, should be something like
    https://gitlab.com/api/v4/projects/1
    """
