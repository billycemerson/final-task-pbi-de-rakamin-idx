"""Load transformed DataFrames into DWH tables."""
import pandas as pd
from sqlalchemy import text

from src.db import get_dwh_engine


def clear_table(table_name: str) -> None:
    """Delete all rows from a table. Call child tables before parent tables
    to respect foreign key constraints."""
    engine = get_dwh_engine()
    with engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {table_name}"))


def load_table(df: pd.DataFrame, table_name: str) -> None:
    df.to_sql(table_name, get_dwh_engine(), if_exists="append", index=False)