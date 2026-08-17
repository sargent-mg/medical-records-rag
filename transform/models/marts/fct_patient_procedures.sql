with procedures as (
    select * from {{ ref('stg_procedures') }}
),

patients as (
    select patient_id, full_name from {{ ref('stg_patients') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['pr.patient_id', 'pr.procedure_code', 'pr.start_date']) }} as procedure_id,
    pr.patient_id,
    p.full_name,
    pr.start_date,
    pr.stop_date,
    pr.procedure_code,
    pr.procedure_description,
    pr.base_cost,
    pr.reason_code,
    pr.reason_description
from procedures pr
left join patients p on pr.patient_id = p.patient_id