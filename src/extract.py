"""Extract raw data from source systems: SQL Server tables, Excel, and CSV.

Each function returns a raw DataFrame with source column names untouched
Renaming/casing happens in transform.py.
"""
import pandas as pd

from src.config import get_settings
from src.db import get_src_engine


def extract_branch() -> pd.DataFrame:
    return pd.read_sql("SELECT branch_id, branch_name, branch_location FROM branch", get_src_engine())


def extract_customer() -> pd.DataFrame:
    query = """
        SELECT c.customer_id, c.customer_name, c.address,
               ci.city_name, s.state_name, c.age, c.gender, c.email
        FROM customer c
        JOIN city ci ON c.city_id = ci.city_id
        JOIN state s ON ci.state_id = s.state_id
    """
    return pd.read_sql(query, get_src_engine())


def extract_account() -> pd.DataFrame:
    query = "SELECT account_id, customer_id, account_type, balance, date_opened, status FROM account"
    return pd.read_sql(query, get_src_engine())


def extract_transaction_db() -> pd.DataFrame:
    query = """
        SELECT transaction_id, account_id, transaction_date, amount, transaction_type, branch_id
        FROM transaction_db
    """
    return pd.read_sql(query, get_src_engine())


def extract_transaction_excel() -> pd.DataFrame:
    return pd.read_excel(get_settings().transaction_excel_path)


def extract_transaction_csv() -> pd.DataFrame:
    return pd.read_csv(get_settings().transaction_csv_path)