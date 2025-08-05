from functools import cache

import papai_unified_storage

from src.configurations import get_storage_config


@cache
def fs():
    storage_config = get_storage_config()
    storage_options = storage_config.storage_options

    fs: papai_unified_storage.storage.Storage = papai_unified_storage.filesystem(
        protocol=storage_config.storage_name, **storage_options.model_dump()
    )
    return fs
