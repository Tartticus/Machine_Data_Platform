
from dagster import ScheduleDefinition
from .jobs import bronze_to_gold_job

bronze_to_gold_schedule = ScheduleDefinition(
    job=bronze_to_gold_job,
    cron_schedule="*/5 * * * *",  # every 5 minutes
)
