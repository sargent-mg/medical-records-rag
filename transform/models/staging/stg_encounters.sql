with source as (
    select * from {{ source('raw', 'encounters') }}
),

renamed as (
    select
        id                                          as encounter_id,
        patient                                     as patient_id,
        start::timestamp                            as start_date,
        stop::timestamp                             as stop_date,
        encounterclass                              as encounter_class,
        code                                        as encounter_code,
        description                                 as encounter_description,
        reasoncode                                  as reason_code,
        reasondescription                           as reason_description,
        base_encounter_cost,
        total_claim_cost,
        payer_coverage
    from source
)

select * from renamed