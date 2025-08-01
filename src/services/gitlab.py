from typing import Any

import httpx
from httpx import URL

from src.services.requests_httpx import request


class GitLabAgent:
    def __init__(self, url: URL, project_id: int, trigger_token: str, ref: str = "main"):
        self.url = url
        self.project_id = project_id
        self.trigger_token = trigger_token
        self.ref = ref

    def trigger_pipeline(self, inputs: dict[str, Any]) -> int:
        """Trigger a GitLab pipeline with the given inputs."""

        params = {"token": self.trigger_token, "ref": self.ref}
        response: httpx.Response = request(
            "post", self.trigger_url, payload=inputs, query_params=params
        )
        return response.json()["id"]

    @property
    def trigger_url(self) -> URL:
        """Get the URL to trigger a pipeline."""
        return self.url.join("trigger/pipeline")
