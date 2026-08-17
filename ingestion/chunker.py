import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

def get_engine():
    return create_engine(DATABASE_URL)

def generate_patient_chunks() -> list[dict]:
    engine = get_engine()
    chunks = []

    # --- Patient summary chunks ---
    summary_df = pd.read_sql("SELECT * FROM marts.fct_patient_summary", engine)
    for _, row in summary_df.iterrows():
        status = "alive" if row["is_alive"] else f"deceased on {row['death_date']}"
        conditions = row["active_conditions"] or "none recorded"
        medications = row["active_medications"] or "none recorded"
        allergies = row["active_allergies"] or "none recorded"

        text = (
            f"Patient: {row['full_name']}, {row['age']} years old, {row['gender']}, "
            f"{row['race']} {row['ethnicity']}, {status}. "
            f"Lives in {row['city']}, {row['state']}. "
            f"Active conditions: {conditions}. "
            f"Current medications: {medications}. "
            f"Known allergies: {allergies}. "
            f"Total encounters: {row['total_encounters']}. "
            f"Last encounter: {row['last_encounter_date']}."
        )
        chunks.append({
            "patient_id": row["patient_id"],
            "full_name": row["full_name"],
            "chunk_type": "summary",
            "text": text,
        })

    # --- Condition chunks ---
    cond_df = pd.read_sql("SELECT * FROM marts.fct_patient_conditions", engine)
    for _, row in cond_df.iterrows():
        status = "active" if row["is_active"] else f"resolved on {row['stop_date']}"
        text = (
            f"Patient {row['full_name']} has condition: {row['condition_description']} "
            f"(code: {row['condition_code']}), diagnosed on {row['start_date']}, status: {status}."
        )
        chunks.append({
            "patient_id": row["patient_id"],
            "full_name": row["full_name"],
            "chunk_type": "condition",
            "text": text,
        })

    # --- Medication chunks ---
    med_df = pd.read_sql("SELECT * FROM marts.fct_patient_medications", engine)
    for _, row in med_df.iterrows():
        status = "active" if row["is_active"] else f"stopped on {row['stop_date']}"
        reason = f" Prescribed for: {row['reason_description']}." if row["reason_description"] else ""
        text = (
            f"Patient {row['full_name']} is prescribed {row['medication_description']} "
            f"(code: {row['medication_code']}), started {row['start_date']}, status: {status}.{reason}"
        )
        chunks.append({
            "patient_id": row["patient_id"],
            "full_name": row["full_name"],
            "chunk_type": "medication",
            "text": text,
        })

    # --- Allergy chunks ---
    allergy_df = pd.read_sql("SELECT * FROM marts.fct_patient_allergies", engine)
    for _, row in allergy_df.iterrows():
        reaction = f" Reaction: {row['reaction_description']} (severity: {row['severity']})." if row["reaction_description"] else ""
        text = (
            f"Patient {row['full_name']} has allergy to {row['allergy_description']} "
            f"(type: {row['allergy_type']}, category: {row['category']}).{reaction}"
        )
        chunks.append({
            "patient_id": row["patient_id"],
            "full_name": row["full_name"],
            "chunk_type": "allergy",
            "text": text,
        })

    # --- Observation chunks (lab results only) ---
    obs_df = pd.read_sql(
        "SELECT * FROM marts.fct_patient_observations WHERE category = 'laboratory'",
        engine
    )
    for _, row in obs_df.iterrows():
        units = f" {row['units']}" if row["units"] else ""
        text = (
            f"Patient {row['full_name']} lab result on {row['observation_date']}: "
            f"{row['observation_description']} = {row['value']}{units}."
        )
        chunks.append({
            "patient_id": row["patient_id"],
            "full_name": row["full_name"],
            "chunk_type": "observation",
            "text": text,
        })

    return chunks

if __name__ == "__main__":
    chunks = generate_patient_chunks()
    print(chunks[0])