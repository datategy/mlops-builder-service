from pathlib import Path

import sqlalchemy.types as types


class SQLPath(types.TypeDecorator):
    impl = types.String

    cache_ok = True

    def process_bind_param(self, value: Path, *_) -> str:
        return value.as_posix()

    def process_result_value(self, value: str, *_) -> Path:
        return Path(value)
