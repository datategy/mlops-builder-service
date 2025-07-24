from collections.abc import Iterator
from functools import cache

from papai_unified_storage import Storage, filesystem

from src.configurations import get_storage_config
from src.utils.exceptions import FilesNotFound


@cache
def get_fs() -> Storage:
    storage_config = get_storage_config()
    storage_options = storage_config.storage_options

    fs = filesystem(protocol=storage_config.storage_name, **storage_options.model_dump())
    return fs


def assert_files_exist(file_paths: list[str] | Iterator[str]):
    fs = get_fs()
    excs = []
    for file_path in file_paths:
        if not fs.exists(file_path):
            excs.append(FileNotFoundError(f"File {file_path} not found."))

    if excs:
        raise FilesNotFound("Files not found.", excs)
