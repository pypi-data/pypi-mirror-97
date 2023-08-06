# coding: utf-8
from gino.ext.starlette import Gino

from modularapi.settings import get_setting

db = Gino(dsn=get_setting().PG_DNS)
