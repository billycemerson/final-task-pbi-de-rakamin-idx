"""ETL job 2: merge transaction_excel, transaction_csv, and transaction_db into the FactTransaction table, 
deduplicated by TransactionID."""
from prefect import flow, task

from src.extract import extract_transaction_csv, extract_transaction_db, extract_transaction_excel
from src.load import clear_table, load_table
from src.transform import merge_transactions

extract_db_task = task(extract_transaction_db)
extract_excel_task = task(extract_transaction_excel)
extract_csv_task = task(extract_transaction_csv)
merge_task = task(merge_transactions)
clear_task = task(clear_table)
load_task = task(load_table)


@flow(name="load_fact_transaction")
def load_fact_transaction() -> None:
    clear_task("FactTransaction")
    db_df = extract_db_task()
    excel_df = extract_excel_task()
    csv_df = extract_csv_task()
    merged = merge_task(db_df, excel_df, csv_df)
    load_task(merged, "FactTransaction")


if __name__ == "__main__":
    load_fact_transaction()