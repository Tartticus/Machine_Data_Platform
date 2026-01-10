

from dagster import asset, AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

DBT_PROJECT_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]  # back to repo root
    / "dbt"
)

@asset(group_name="bronze")
def bronze_machine_events():
    """Raw machine events ingested from Kafka into Postgres."""
    # Ingestion is handled by the Kafka consumer.
    return


@dbt_assets(
    manifest=str(DBT_PROJECT_DIR / "target" / "manifest.json"),
)
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    # Explicitly select the models we care about in the CLI call
    yield from dbt.cli(
        ["build", "--select", "silver_machine_events machine_hourly_stats"],
        context=context,
    ).stream()
