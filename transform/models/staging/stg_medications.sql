with source as (
    select * from {{ source('raw', 'medications') }}
),

deduped as (
    select distinct on (patient, code, start, encounter)
        patient,
        encounter,
        start,
        stop,
        code,
        description,
        base_cost,
        dispenses,
        totalcost,
        reasondescription
    from source
    order by patient, code, start, encounter
),

renamed as (
    select
        patient                                     as patient_id,
        encounter                                   as encounter_id,
        start::timestamp                            as start_date,
        stop::timestamp                             as stop_date,
        code                                        as medication_code,
        description                                 as medication_description,
        base_cost,
        dispenses,
        totalcost                                   as total_cost,
        reasondescription                           as reason_description,
        case
            when stop is null then true
            else false
        end                                         as is_active
    from deduped
)

select * from renamed