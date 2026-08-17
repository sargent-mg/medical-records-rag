import os
from prefect import flow, task
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from dotenv import load_dotenv
from ingestion.load_raw import load_all

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DBT_PROJECT_DIR = os.path.join(PROJECT_ROOT, "transform")

@task(name="load-raw-csvs", retries=2)
def load_raw_csvs():
    load_all()

@task(name="run-dbt")
def run_dbt():
    trigger_dbt_cli_command.fn(
        command="dbt run",
        project_dir=DBT_PROJECT_DIR,
        profiles_dir=DBT_PROJECT_DIR,
        create_summary_artifact=False,
    )

@task(name="run-dbt-tests")
def run_dbt_tests():
    trigger_dbt_cli_command.fn(
        command="dbt test",
        project_dir=DBT_PROJECT_DIR,
        profiles_dir=DBT_PROJECT_DIR,
        create_summary_artifact=False,
    )

@flow(name="medical-records-ingestion")
def ingestion_pipeline():
    load_raw_csvs()
    run_dbt()
    run_dbt_tests()

if __name__ == "__main__":
    ingestion_pipeline()