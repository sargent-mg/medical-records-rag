with source as (
    select * from {{ source('raw', 'patients') }}
),

renamed as (
    select
        id                                          as patient_id,
        first || ' ' || last                        as full_name,
        first                                       as first_name,
        last                                        as last_name,
        prefix,
        suffix,
        birthdate::date                             as birth_date,
        deathdate::date                             as death_date,
        case
            when deathdate is null then true
            else false
        end                                         as is_alive,
        marital,
        race,
        ethnicity,
        gender,
        birthplace,
        city,
        state,
        zip
    from source
)

select * from renamed