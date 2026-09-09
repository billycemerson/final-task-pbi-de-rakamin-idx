"""SQLAlchemy engine factory for databases."""
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config import get_settings


@lru_cache
def get_src_engine() -> Engine:
    return create_engine(get_settings().src_conn_str)


@lru_cache
def get_dwh_engine() -> Engine:
    return create_engine(get_settings().dwh_conn_str)