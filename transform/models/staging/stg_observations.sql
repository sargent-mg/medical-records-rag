with source as (
    select * from {{ source('raw', 'observations') }}
),

deduped as (
    select distinct on (patient, code, date, encounter)
        patient,
        encounter,
        date,
        category,
        code,
        description,
        value,
        units,
        type
    from source
    where value is not null
    order by patient, code, date, encounter
),

renamed as (
    select
        patient                                     as patient_id,
        encounter                                   as encounter_id,
        date::timestamp                             as observation_date,
        category,
        code                                        as observation_code,
        description                                 as observation_description,
        value,
        units,
        type                                        as value_type
    from deduped
)

select * from renamed