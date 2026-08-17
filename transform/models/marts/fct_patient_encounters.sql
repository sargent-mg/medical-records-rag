with encounters as (
    select * from {{ ref('stg_encounters') }}
),

patients as (
    select patient_id, full_name from {{ ref('stg_patients') }}
)

select
    e.encounter_id,
    e.patient_id,
    p.full_name,
    e.start_date,
    e.stop_date,
    e.encounter_class,
    e.encounter_code,
    e.encounter_description,
    e.reason_code,
    e.reason_description,
    e.base_encounter_cost,
    e.total_claim_cost,
    e.payer_coverage
from encounters e
left join patients p on e.patient_id = p.patient_id