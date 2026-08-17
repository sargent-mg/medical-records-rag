with source as (
    select * from {{ source('raw', 'conditions') }}
),

renamed as (
    select
        patient                                     as patient_id,
        encounter                                   as encounter_id,
        start::date                                 as start_date,
        stop::date                                  as stop_date,
        code                                        as condition_code,
        description                                 as condition_description,
        case
            when stop is null then true
            else false
        end                                         as is_active
    from source
)

select * from renamed