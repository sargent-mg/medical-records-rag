with patients as (
    select * from {{ ref('stg_patients') }}
),

conditions as (
    select
        patient_id,
        count(*) filter (where is_active)           as active_condition_count,
        count(*) filter (where not is_active)       as resolved_condition_count,
        string_agg(
            condition_description,
            ', ' order by start_date desc
        ) filter (where is_active)                  as active_conditions
    from {{ ref('stg_conditions') }}
    group by patient_id
),

medications as (
    select
        patient_id,
        count(*) filter (where is_active)           as active_medication_count,
        string_agg(
            medication_description,
            ', ' order by start_date desc
        ) filter (where is_active)                  as active_medications
    from {{ ref('stg_medications') }}
    group by patient_id
),

allergies as (
    select
        patient_id,
        count(*) filter (where is_active)           as active_allergy_count,
        string_agg(
            allergy_description,
            ', ' order by start_date desc
        ) filter (where is_active)                  as active_allergies
    from {{ ref('stg_allergies') }}
    group by patient_id
),

encounters as (
    select
        patient_id,
        count(*)                                    as total_encounters,
        max(start_date)                             as last_encounter_date
    from {{ ref('stg_encounters') }}
    group by patient_id
)

select
    p.patient_id,
    p.full_name,
    p.first_name,
    p.last_name,
    p.birth_date,
    p.death_date,
    p.is_alive,
    date_part('year', age(
        coalesce(p.death_date, current_date), p.birth_date
    ))::int                                         as age,
    p.gender,
    p.race,
    p.ethnicity,
    p.marital,
    p.city,
    p.state,
    coalesce(c.active_condition_count, 0)           as active_condition_count,
    coalesce(c.resolved_condition_count, 0)         as resolved_condition_count,
    c.active_conditions,
    coalesce(m.active_medication_count, 0)          as active_medication_count,
    m.active_medications,
    coalesce(a.active_allergy_count, 0)             as active_allergy_count,
    a.active_allergies,
    coalesce(e.total_encounters, 0)                 as total_encounters,
    e.last_encounter_date
from patients p
left join conditions c on p.patient_id = c.patient_id
left join medications m on p.patient_id = m.patient_id
left join allergies a on p.patient_id = a.patient_id
left join encounters e on p.patient_id = e.patient_id