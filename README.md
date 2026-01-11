# Machine_Data_Platform
End-to-end simulated machine data platform using Modbus, Kafka, Postgres, dbt (for silver/gold tables), orchestrated by Dagster and Kubernetes, with superset for analytics


This project simulates a real industrial data pipeline where machine telemetry is ingested from a PLC-style Modbus interface, streamed through Kafka, materialized into a bronze/silver/gold warehouse model using dbt orchestrated by Dagster, and visualized via Superset.

It was built as a learning project to explore how modern data-centric companies deploy and operate data systems using containerization, orchestration, and streaming-first architectures.

<img width="1325" height="736" alt="image" src="https://github.com/user-attachments/assets/e87c72cf-07bb-4e6a-8656-851c3a2bfd38" />

<img width="2101" height="644" alt="image" src="https://github.com/user-attachments/assets/d07e95e9-27a1-4003-9c23-c53ecf9cc1e7" />
<img width="1118" height="564" alt="image" src="https://github.com/user-attachments/assets/d0a184f0-0e66-4590-aa10-69c0cbd13a5e" />




