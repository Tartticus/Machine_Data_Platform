# change bronze table to gold table

from dagster import define_asset_job, AssetSelection

bronze_to_gold_job = define_asset_job(
    "bronze_to_gold_job",
    selection=AssetSelection.keys(
        "bronze_machine_events",
        "silver_machine_events",
        "machine_hourly_stats",
    ),
)