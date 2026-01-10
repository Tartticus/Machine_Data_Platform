
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    event_natural_key as unique_field,
    count(*) as n_records

from "machines"."analytics"."silver_machine_events"
where event_natural_key is not null
group by event_natural_key
having count(*) > 1



  
  
      
    ) dbt_internal_test