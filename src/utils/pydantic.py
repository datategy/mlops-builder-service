from typing import Annotated

from httpx import URL
from pydantic import AnyUrl, BeforeValidator, HttpUrl, TypeAdapter

AnyUrlTypeAdapter = TypeAdapter(AnyUrl)
AnyHttpxURL = Annotated[
    URL, BeforeValidator(lambda value: AnyUrlTypeAdapter.validate_python(str(value)) and URL(value))
]
"""This type requires setting config `arbitrary_types_allowed` to `True`."""

HttpUrlTypeAdapter = TypeAdapter(HttpUrl)
HttpxURL = Annotated[
    URL,
    BeforeValidator(lambda value: HttpUrlTypeAdapter.validate_python(str(value)) and URL(value)),
]
"""This type requires setting config `arbitrary_types_allowed` to `True`."""
