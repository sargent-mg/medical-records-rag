with conditions as (
    select * from {{ ref('stg_conditions') }}
),

patients as (
    select patient_id, full_name from {{ ref('stg_patients') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['c.patient_id', 'c.condition_code', 'c.start_date']) }} as condition_id,
    c.patient_id,
    p.full_name,
    c.condition_code,
    c.condition_description,
    c.start_date,
    c.stop_date,
    c.is_active
from conditions c
left join patients p on c.patient_id = p.patient_id