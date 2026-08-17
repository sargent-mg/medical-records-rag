with observations as (
    select * from {{ ref('stg_observations') }}
),

patients as (
    select patient_id, full_name from {{ ref('stg_patients') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['o.patient_id', 'o.observation_code', 'o.observation_date', 'o.encounter_id']) }} as observation_id,
    o.patient_id,
    o.encounter_id,
    p.full_name,
    o.observation_date,
    o.category,
    o.observation_code,
    o.observation_description,
    o.value,
    o.units,
    o.value_type
from observations o
left join patients p on o.patient_id = p.patient_id