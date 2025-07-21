from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.pydantic import AnyHttpxURL


class GitLabTrigger(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="gitlab_", arbitrary_types_allowed=True)

    project_url: AnyHttpxURL
    """
    URL that points to a project, should be something like https://gitlab.com/api/v4/projects/1
    """
    trigger_token: SecretStr = SecretStr("")
    """GitLab trigger token. See https://docs.gitlab.com/ci/triggers/"""
    ref: str = "main"
    """Branch or tag to trigger the pipeline on."""
