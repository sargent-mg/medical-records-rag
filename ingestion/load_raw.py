import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

SENSITIVE_COLUMNS = ["SSN", "DRIVERS", "PASSPORT"]

CSV_FILES = [
    "patients",
    "conditions",
    "medications",
    "observations",
    "allergies",
    "encounters",
    "procedures",
]

def get_engine():
    return create_engine(DATABASE_URL)

def load_csv_to_postgres(table_name: str, engine) -> int:
    path = f"data/raw/{table_name}.csv"
    df = pd.read_csv(path, low_memory=False)

    # Drop sensitive columns if present
    cols_to_drop = [c for c in SENSITIVE_COLUMNS if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    # Normalize column names to lowercase
    df.columns = [c.lower() for c in df.columns]

    df.to_sql(table_name, engine, if_exists="replace", index=False)
    return len(df)

def load_all():
    engine = get_engine()
    for table in CSV_FILES:
        count = load_csv_to_postgres(table, engine)
        print(f"Loaded {count} rows into {table}")

if __name__ == "__main__":
    load_all()
