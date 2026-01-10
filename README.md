# Machine_Data_Platform
End-to-end simulated machine data platform using Modbus, Kafka, Postgres, dbt (for silver/gold tables), orchestrated by Dagster and Kubernetes, with superset for analytics


This project simulates a real industrial data pipeline where machine telemetry is ingested from a PLC-style Modbus interface, streamed through Kafka, materialized into a bronze/silver/gold warehouse model using dbt orchestrated by Dagster, and visualized via Superset.

It was built as a learning project to explore how modern data-centric companies deploy and operate data systems using containerization, orchestration, and streaming-first architectures.

