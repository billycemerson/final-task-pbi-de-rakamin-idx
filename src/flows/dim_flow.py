"""ETL job 1: load source data into DimBranch, DimCustomer, DimAccount."""
from prefect import flow, task

from src.extract import extract_account, extract_branch, extract_customer
from src.load import clear_table, load_table
from src.transform import transform_account, transform_branch, transform_customer

extract_branch_task = task(extract_branch)
extract_customer_task = task(extract_customer)
extract_account_task = task(extract_account)
transform_branch_task = task(transform_branch)
transform_customer_task = task(transform_customer)
transform_account_task = task(transform_account)
clear_task = task(clear_table)
load_task = task(load_table)


@flow(name="load_dimension_tables")
def load_dimensions() -> None:
    # Clear child tables before parent tables (FK order)
    clear_task("DimAccount")
    clear_task("DimCustomer")
    clear_task("DimBranch")

    load_task(transform_branch_task(extract_branch_task()), "DimBranch")
    load_task(transform_customer_task(extract_customer_task()), "DimCustomer")
    load_task(transform_account_task(extract_account_task()), "DimAccount")


if __name__ == "__main__":
    load_dimensions()