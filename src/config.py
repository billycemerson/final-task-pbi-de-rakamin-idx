"""Environment-based configuration for DB connections and flat-file paths.
All connection details are stored in `.env`.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _build_conn_str(server: str, database: str) -> str:
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").replace(" ", "+")
    if os.getenv("DB_TRUSTED_CONNECTION", "yes").lower() == "yes":
        return f"mssql+pyodbc://{server}/{database}?driver={driver}&trusted_connection=yes"
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    return f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver}"


@dataclass(frozen=True)
class Settings:
    src_conn_str: str
    dwh_conn_str: str
    transaction_excel_path: str
    transaction_csv_path: str


def get_settings() -> Settings:
    return Settings(
        src_conn_str=_build_conn_str(
            os.getenv("SRC_DB_SERVER", "localhost"),
            os.getenv("SRC_DB_NAME", "sample"),
        ),
        dwh_conn_str=_build_conn_str(
            os.getenv("DWH_DB_SERVER", "localhost"),
            os.getenv("DWH_DB_NAME", "DWH"),
        ),
        transaction_excel_path=os.getenv("TRANSACTION_EXCEL_PATH", "data/transaction_excel.xlsx"),
        transaction_csv_path=os.getenv("TRANSACTION_CSV_PATH", "data/transaction_csv.csv"),
    )