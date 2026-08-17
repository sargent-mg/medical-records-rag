with medications as (
    select * from {{ ref('stg_medications') }}
),

patients as (
    select patient_id, full_name from {{ ref('stg_patients') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['m.patient_id', 'm.medication_code', 'm.start_date', 'm.encounter_id']) }} as medication_id,
    m.patient_id,
    m.encounter_id,
    p.full_name,
    m.medication_code,
    m.medication_description,
    m.start_date,
    m.stop_date,
    m.is_active,
    m.base_cost,
    m.dispenses,
    m.total_cost,
    m.reason_description
from medications m
left join patients p on m.patient_id = p.patient_id