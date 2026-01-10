# Machine_Data_Platform
End-to-end simulated machine data platform using Modbus, Kafka, Postgres, dbt (for silver/gold tables), orchestrated by Dagster and Kubernetes, with superset for analytics


This project simulates a real industrial data pipeline where machine telemetry is ingested from a PLC-style Modbus interface, streamed through Kafka, materialized into a bronze/silver/gold warehouse model using dbt orchestrated by Dagster, and visualized via Superset.

It was built as a learning project to explore how modern data-centric companies deploy and operate data systems using containerization, orchestration, and streaming-first architectures.
<img width="785" height="597" alt="image" src="https://github.com/user-attachments/assets/8452c7b3-e4bd-4df8-83e5-c2f3addda0a6" />
<img width="785" height="597" alt="image" src="https://github.com/user-attachments/assets/9bcfa214-7873-48bb-9261-3c9b58099e24" />
<img width="785" height="597" alt="image" src="https://github.com/user-attachments/assets/427dadf6-466d-4480-99e0-016e53a2f30d" />
