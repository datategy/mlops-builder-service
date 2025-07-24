from pydantic_settings import BaseSettings, SettingsConfigDict

from src.schemas.molecules.gitlab import GitLabTriggerConfig


class BuildAgentConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="build_agent_", env_nested_delimiter="__")

    model_interface = GitLabTriggerConfig
    model_instance: GitLabTriggerConfig
