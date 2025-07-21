from dataclasses import asdict, dataclass
from typing import Any

import httpx

from src.configurations import get_general_config
from src.services.requests_httpx import request


@dataclass
class GitLabVariable:
    key: str
    value: str


def dict_to_gitlab_variables(input: dict[str, Any]) -> list[GitLabVariable]:
    gitlab_variables = []
    for k, v in input.items():
        gitlab_variables.append(GitLabVariable(k, v))
    return gitlab_variables


def get_pipeline_jobs_url(pipeline_id: int) -> str:
    """https://docs.gitlab.com/ee/api/jobs.html#list-pipeline-jobs"""
    return f"{get_general_config().gitlab_project_url}/pipelines/{pipeline_id}/jobs"


def get_job_trace_url(job_id: int) -> str:
    """https://docs.gitlab.com/ee/api/jobs.html#get-a-log-file"""
    return f"{get_general_config().gitlab_project_url}/jobs/{job_id}/trace"


def get_one_pipeline_url(pipeline_id: int) -> str:
    """https://docs.gitlab.com/ee/api/pipelines.html#get-a-single-pipeline"""
    return f"{get_general_config().gitlab_project_url}/pipelines/{pipeline_id}"


def post_pipeline_creation_url() -> str:
    """https://docs.gitlab.com/ee/api/pipelines.html#create-a-new-pipeline"""
    return f"{get_general_config().gitlab_project_url}/pipeline"


def gitlab_request(url: str, json: dict | None = None) -> httpx.Response:
    gitlab_token = get_general_config().gitlab_private_token.get_secret_value()
    response = request("post", url, payload=json, headers={"PRIVATE-TOKEN": gitlab_token})
    return response


def fetch_pipeline_job_ids(pipeline_id: int) -> list[int]:
    """Fetch the jobs of a GitLab pipeline."""
    response = gitlab_request("get", get_pipeline_jobs_url(pipeline_id))
    jobs = response.json()
    return [job["id"] for job in jobs]


def fetch_pipeline_logs(pipeline_id: int) -> str:
    """Fetch logs of all the jobs for a GitLab pipeline."""
    job_ids = fetch_pipeline_job_ids(pipeline_id)

    logs = [""] * len(job_ids)
    for i, job_id in enumerate(job_ids):
        response = gitlab_request("get", get_job_trace_url(job_id))
        logs[i] = response.text

    return "\n".join(logs)


def run_pipeline(variables: dict[str, str]) -> int:
    """Run a GitLab pipeline.

    Parameters
    ----------
    variables : dict[str, str]
        The variables to be used in the pipeline.

    Returns
    -------
    int
        The ID of the pipeline that was created.
    """
    variables = dict_to_gitlab_variables(variables)

    payload = [asdict(var) for var in variables]
    response: httpx.Response = gitlab_request("post", post_pipeline_creation_url(), json=payload)
    return response.json()["id"]
