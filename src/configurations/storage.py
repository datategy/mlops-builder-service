from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageParameters(BaseModel):
    model_config = ConfigDict(extra="allow")


POSSIBLE_STORAGE = Literal[
    "abfs",
    "adl",
    "arrow_hdfs",
    "asynclocal",
    "az",
    "blockcache",
    "box",
    "cached",
    "dask",
    "data",
    "dbfs",
    "dir",
    "dropbox",
    "dvc",
    "file",
    "filecache",
    "ftp",
    "gcs",
    "gdrive",
    "generic",
    "git",
    "github",
    "gs",
    "hdfs",
    "hf",
    "http",
    "https",
    "jlab",
    "jupyter",
    "lakefs",
    "libarchive",
    "local",
    "memory",
    "oci",
    "ocilake",
    "oss",
    "reference",
    "root",
    "s3",
    "s3a",
    "sftp",
    "simplecache",
    "smb",
    "ssh",
    "tar",
    "wandb",
    "webdav",
    "webhdfs",
    "zip",
]


class StorageConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="storage_", env_nested_delimiter="__")

    name: POSSIBLE_STORAGE = "file"
    """Storage implementation to use.

    See https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations
    and https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations
    for a list of possible values.
    """
    options: StorageParameters = StorageParameters()
    """Options used to instanciate the storage class corresponding to `STORAGE_NAME`.

    All the env var that start with this pattern are passed to the storage class
    `__init__` function as keyword arguments. The name of the option should be
    written in all caps after `STORAGE_OPTIONS__` e.g.
    `STORAGE_OPTIONS__SECRET_KEY="thisisasecretkey"` will be passed as
    `fsspec.filesystem(storage_name, secret_key="thisisasecretkey")`.
    """
