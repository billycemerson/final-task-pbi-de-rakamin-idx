"""Quick connectivity check for both databases."""
from sqlalchemy import text

from src.db import get_dwh_engine, get_src_engine


def check_connection(engine, label: str) -> None:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"[OK] Connected to {label}")
    except Exception as e:
        print(f"[FAIL] Could not connect to {label}: {e}")


if __name__ == "__main__":
    check_connection(get_src_engine(), "source (sample)")
    check_connection(get_dwh_engine(), "DWH")