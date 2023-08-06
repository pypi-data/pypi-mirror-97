# coding: utf-8
import os
import logging
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Setting(BaseSettings):
    ENVIRONMENT: str = "developpment"
    PG_DNS: PostgresDsn

    LOG_TO_STDOUT: bool = True
    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FMT: str = "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"


@lru_cache()
def get_setting() -> Setting:
    try:
        setting = Setting(
            _env_file=os.environ.get("DOTENV_PATH", ".env"),
            _env_file_encoding="utf-8",
        )
    except KeyError:
        setting = Setting()
    return setting
