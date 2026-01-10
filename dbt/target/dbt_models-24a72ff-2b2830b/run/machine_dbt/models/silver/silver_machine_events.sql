
      
        
        
        delete from "machines"."analytics"."silver_machine_events" as DBT_INTERNAL_DEST
        where (event_natural_key) in (
            select distinct event_natural_key
            from "silver_machine_events__dbt_tmp155026169253" as DBT_INTERNAL_SOURCE
        );

    

    insert into "machines"."analytics"."silver_machine_events" ("event_natural_key", "ts", "machine_id", "temperature", "pressure", "rpm", "fault_code")
    (
        select "event_natural_key", "ts", "machine_id", "temperature", "pressure", "rpm", "fault_code"
        from "silver_machine_events__dbt_tmp155026169253"
    )
  