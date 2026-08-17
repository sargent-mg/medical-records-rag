with source as (
    select * from {{ source('raw', 'allergies') }}
),

renamed as (
    select
        patient                                     as patient_id,
        encounter                                   as encounter_id,
        start::date                                 as start_date,
        case when stop::text ~ '^\d{4}-\d{2}-\d{2}' then stop::text::date else null end as stop_date,
        code                                        as allergy_code,
        description                                 as allergy_description,
        type                                        as allergy_type,
        category,
        reaction1                                   as reaction,
        description1                                as reaction_description,
        severity1                                   as severity,
        case
            when stop is null then true
            else false
        end                                         as is_active
    from source
)

select * from renamed