"""Transform raw extracts into DWH-ready shapes, including renaming, casing, and deduplication."""
import pandas as pd

_UPPER_CUSTOMER_COLS = ["CustomerName", "Address", "CityName", "StateName", "Gender"]


def transform_branch(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "branch_id": "BranchID",
        "branch_name": "BranchName",
        "branch_location": "BranchLocation",
    })
    return df[["BranchID", "BranchName", "BranchLocation"]]


def transform_customer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "customer_id": "CustomerID",
        "customer_name": "CustomerName",
        "address": "Address",
        "city_name": "CityName",
        "state_name": "StateName",
        "age": "Age",
        "gender": "Gender",
        "email": "Email",
    })
    # Uppercase everything except CustomerID, Age, Email - per spec
    df[_UPPER_CUSTOMER_COLS] = df[_UPPER_CUSTOMER_COLS].apply(lambda col: col.str.upper())
    return df[["CustomerID", "CustomerName", "Address", "CityName", "StateName", "Age", "Gender", "Email"]]


def transform_account(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "account_id": "AccountID",
        "customer_id": "CustomerID",
        "account_type": "AccountType",
        "balance": "Balance",
        "date_opened": "DateOpened",
        "status": "Status",
    })
    return df[["AccountID", "CustomerID", "AccountType", "Balance", "DateOpened", "Status"]]


def _standardize_transaction_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "transaction_id": "TransactionID",
        "account_id": "AccountID",
        "transaction_date": "TransactionDate",
        "amount": "Amount",
        "transaction_type": "TransactionType",
        "branch_id": "BranchID",
    })
    df = df[["TransactionID", "AccountID", "TransactionDate", "Amount", "TransactionType", "BranchID"]]
    # transaction_db returns proper Timestamps already; excel/csv give strings
    # like "22-01-2024 10:20:00" (DD-MM-YYYY). dayfirst=True handles both.
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], dayfirst=True)
    return df


def merge_transactions(db_df: pd.DataFrame, excel_df: pd.DataFrame, csv_df: pd.DataFrame) -> pd.DataFrame:
    """Combine the three transaction sources, dropping duplicate TransactionID rows."""
    frames = [_standardize_transaction_columns(df) for df in (db_df, excel_df, csv_df)]
    combined = pd.concat(frames, ignore_index=True)
    return combined.drop_duplicates(subset="TransactionID", keep="first")