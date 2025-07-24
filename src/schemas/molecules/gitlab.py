from httpx import URL
from pydantic import BaseModel, ConfigDict, SecretStr

from src.utils.pydantic import AnyHttpxURL


class GitLabTriggerConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    host: AnyHttpxURL = URL("https://gitlab.com")
    """
    URL that points to the gitlab host.
    """
    project_id: int = 1
    """
    ID of the GitLab project to trigger pipelines in. It is the last digit in
    the URL https://gitlab.com/api/v4/projects/1
    """
    trigger_token: SecretStr = SecretStr("")
    """token to trigger the GitLab pipeline."""
    ref: str = "main"
    """GitLab branch to trigger the pipeline on."""
