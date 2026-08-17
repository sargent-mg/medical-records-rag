import os
import subprocess
from prefect import flow, task
from dotenv import load_dotenv
from ingestion.load_raw import load_all

load_dotenv()

@task(name="load-raw-csvs", retries=2)
def load_raw_csvs():
    load_all()

@task(name="run-dbt", retries=1)
def run_dbt():
    env = os.environ.copy()
    result = subprocess.run(
        [".venv/bin/dbt", "run", "--profiles-dir", "transform"],
        capture_output=True,
        text=True,
        env=env
    )
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"dbt run failed:\n{result.stderr}")

@task(name="run-dbt-tests", retries=0)
def run_dbt_tests():
    env = os.environ.copy()
    result = subprocess.run(
        [".venv/bin/dbt", "test", "--profiles-dir", "transform"],
        capture_output=True,
        text=True,
        env=env
    )
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"dbt test failed:\n{result.stderr}")

@flow(name="medical-records-ingestion")
def ingestion_pipeline():
    load_raw_csvs()
    run_dbt()
    run_dbt_tests()

if __name__ == "__main__":
    ingestion_pipeline()