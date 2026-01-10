
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select machine_id
from "machines"."analytics"."machine_hourly_stats"
where machine_id is null



  
  
      
    ) dbt_internal_test