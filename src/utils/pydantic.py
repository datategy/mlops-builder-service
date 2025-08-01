from pathlib import Path
from typing import Annotated

from httpx import URL
from pydantic import AnyUrl, BeforeValidator, HttpUrl, PlainSerializer, TypeAdapter

AnyUrlTypeAdapter = TypeAdapter(AnyUrl)
AnyHttpxURL = Annotated[
    URL, BeforeValidator(lambda value: AnyUrlTypeAdapter.validate_python(str(value)) and URL(value))
]
"""This type requires setting config `arbitrary_types_allowed` to `True`."""

AnyURLAsStr = Annotated[
    str, BeforeValidator(lambda value: AnyUrlTypeAdapter.validate_python(value) and str(value))
]

HttpUrlTypeAdapter = TypeAdapter(HttpUrl)
HttpxURL = Annotated[
    URL,
    BeforeValidator(lambda value: HttpUrlTypeAdapter.validate_python(str(value)) and URL(value)),
]
"""This type requires setting config `arbitrary_types_allowed` to `True`."""

PathSerializedAsStr = Annotated[Path, PlainSerializer(lambda x: x.as_posix(), return_type=str)]
