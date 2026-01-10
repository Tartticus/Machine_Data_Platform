from dagster import Definitions

from .assets import bronze_machine_events, dbt_models
from .resources import postgres_resource, dbt_resource
from .jobs import bronze_to_gold_job
from .schedules import bronze_to_gold_schedule

# dbt_models is a single AssetsDefinition in this dagster-dbt version
all_assets = [bronze_machine_events, dbt_models]

defs = Definitions(
    assets=all_assets,
    resources={
        "postgres_resource": postgres_resource,
        "dbt": dbt_resource,
    },
    jobs=[bronze_to_gold_job],
    schedules=[bronze_to_gold_schedule],
)
