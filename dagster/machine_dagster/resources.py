# dagster/machine_dagster/resources.py

import psycopg2
from contextlib import contextmanager
from dagster import resource

from dagster_dbt import DbtCliResource
from pathlib import Path


DBT_PROJECT_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]  # back to repo root
    / "dbt"
)

DBT_EXECUTABLE = r"C:\Users\matth\miniconda3\Scripts\dbt.exe"


@resource
def dbt_resource(_):
    return DbtCliResource(
        project_dir=str(DBT_PROJECT_DIR),
        profiles_dir=str(Path.home() / ".dbt"),
        dbt_executable=DBT_EXECUTABLE,
    )

@resource
def postgres_resource(_):
    conn = psycopg2.connect(
        dbname="machines",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port=5432,
    )
    conn.autocommit = False
    return conn


