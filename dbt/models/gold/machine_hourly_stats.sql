{{ config(materialized='table') }}

select
    machine_id,
    date_trunc('hour', ts) as hour,
    avg(temperature) as avg_temperature,
    avg(pressure)    as avg_pressure,
    avg(rpm)         as avg_rpm,
    sum(case when fault_code != 0 then 1 else 0 end) as fault_count
from {{ ref('silver_machine_events') }}
group by 1, 2
