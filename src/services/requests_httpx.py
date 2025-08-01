import time
from typing import Any, Literal

import httpx

from src.schemas.atoms.has_under_str import HasDunderStr
from src.utils.exceptions import MaxRetryErrors


class RetryTransport(httpx.HTTPTransport):
    def __init__(
        self,
        max_retry_on_connection_issue,
        retry_backoff_factor,
        max_retry_on_status,
        retry_status_forcelist,
        *args,
        **kwargs,
    ):
        super().__init__(*args, retries=max_retry_on_connection_issue, **kwargs)
        self.retry_backoff_factor = retry_backoff_factor
        self.max_retry_on_status = max_retry_on_status
        self.retry_status_forcelist = retry_status_forcelist
        self.exception_group = []
        self.current_retry = 0

    def clean_self(self):
        self.exception_group = []
        self.current_retry = 0

    def sleep_with_backoff(self):
        sleep_time = self.retry_backoff_factor * (2 ** (self.current_retry - 1))
        time.sleep(sleep_time)

    def __handle_request(self, request: httpx.Request) -> httpx.Response:
        response = super().handle_request(request)

        if response.status_code in self.retry_status_forcelist:
            self.current_retry += 1
            self.exception_group.append(
                httpx.HTTPStatusError("", request=request, response=response)
            )

            if self.current_retry >= self.max_retry_on_status:
                raise MaxRetryErrors("Max retries reached", self.exception_group)

            self.sleep_with_backoff()
            self.__handle_request(request)

        return response

    def handle_request(self, request) -> httpx.Response:
        self.clean_self()
        response = self.__handle_request(request)
        return response


def request(
    method: Literal["get", "put", "post"],
    url: str | httpx.URL | HasDunderStr,
    payload: dict[str, Any] | None = None,
    query_params: dict[str, Any] | None = None,
    headers: dict | None = None,
    transport: RetryTransport | None = None,
    raise_for_status: bool = True,
) -> httpx.Response:
    if headers is None:
        headers = {}

    if not isinstance(url, (str, httpx.URL)):
        url = str(url)

    if method == "get" and payload is not None:
        raise ValueError("GET requests should not have a payload")

    with httpx.Client(transport=transport) as client:
        response = client.request(
            method=method, url=url, params=query_params, json=payload, headers=headers
        )

    if raise_for_status:
        response.raise_for_status()

    return response
