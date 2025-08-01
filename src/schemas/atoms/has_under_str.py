from typing import Protocol


class HasDunderStr(Protocol):
    def __str__(self) -> str: ...
