# coding: utf-8
import os
import logging
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn

print(os.environ["DOTENV_PATH"])


class Setting(BaseSettings):
    ENVIRONMENT: str = "developpment"
    PG_DNS: PostgresDsn

    LOG_TO_STDOUT: bool = True
    LOGGING_LEVEL: int = logging.INFO


@lru_cache()
def get_setting() -> Setting:
    setting = Setting(
        _env_file=os.environ.get("DOTENV_PATH", ".env"), _env_file_encoding="utf-8"
    )
    return setting
