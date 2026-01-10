
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select hour
from "machines"."analytics"."machine_hourly_stats"
where hour is null



  
  
      
    ) dbt_internal_test