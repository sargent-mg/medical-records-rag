with allergies as (
    select * from {{ ref('stg_allergies') }}
),

patients as (
    select patient_id, full_name from {{ ref('stg_patients') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['a.patient_id', 'a.allergy_code', 'a.start_date']) }} as allergy_id,
    a.patient_id,
    p.full_name,
    a.allergy_code,
    a.allergy_description,
    a.allergy_type,
    a.category,
    a.reaction,
    a.reaction_description,
    a.severity,
    a.start_date,
    a.stop_date,
    a.is_active
from allergies a
left join patients p on a.patient_id = p.patient_id