
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select event_natural_key
from "machines"."analytics"."silver_machine_events"
where event_natural_key is null



  
  
      
    ) dbt_internal_test