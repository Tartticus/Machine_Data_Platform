{{ config(
    materialized='incremental',
    unique_key='event_natural_key'
) }}

with raw as (
    select
        id,
        ts,
        machine_id,
        temperature::int    as temperature,
        pressure::int       as pressure,
        rpm::int            as rpm,
        fault_code::int     as fault_code
    from {{ source('machines', 'bronze_machine_events') }}
),


enriched as (
    select
        md5(id::text) as event_natural_key,
        ts,
        machine_id,
        temperature,
        pressure,
        rpm,
        fault_code
    from raw
)

select *
from enriched

{% if is_incremental() %}
where ts > (select coalesce(max(ts), '1900-01-01') from {{ this }})
{% endif %}