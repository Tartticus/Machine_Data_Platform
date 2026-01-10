import json
import logging
import time
import os
from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2.extras import Json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka_consumer_bronze")

KAFKA_BOOTSTRAP_SERVERS = "127.0.0.1:9092"
KAFKA_TOPIC = "raw_machine_events"
KAFKA_GROUP_ID = "bronze-consumer-group"

PG_CONN_INFO = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "dbname": os.getenv("POSTGRES_DB", "machines"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
}

def create_pg_conn():
    conn = psycopg2.connect(**PG_CONN_INFO)
    conn.autocommit = False
    return conn


def ensure_bronze_table(conn):
    ddl = """
    CREATE TABLE IF NOT EXISTS bronze_machine_events (
        id          BIGSERIAL PRIMARY KEY,
        ts          TIMESTAMPTZ NOT NULL,
        machine_id  INT NOT NULL,
        temperature INT,
        pressure    INT,
        rpm         INT,
        fault_code  INT,
        raw_event   JSONB
    );
    """
    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()
    logger.info("Ensured bronze_machine_events table exists")


def create_kafka_consumer() -> Consumer:
    conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": KAFKA_GROUP_ID,
        "auto.offset.reset": "earliest",
    }
    return Consumer(conf)


def main():
    # Connect to Postgres
    conn = create_pg_conn()
    ensure_bronze_table(conn)

    consumer = create_kafka_consumer()
    consumer.subscribe([KAFKA_TOPIC])

    logger.info(
        f"Starting bronze consumer. Kafka: {KAFKA_BOOTSTRAP_SERVERS}, topic: {KAFKA_TOPIC}, "
        f"group: {KAFKA_GROUP_ID}, Postgres: {PG_CONN_INFO['host']}:{PG_CONN_INFO['port']}/{PG_CONN_INFO['dbname']}"
    )

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                logger.error(f"Kafka error: {msg.error()}")
                continue

            try:
                payload = json.loads(msg.value().decode("utf-8"))
            except Exception as e:
                logger.error(f"Failed to decode message: {e}, raw={msg.value()!r}")
                continue

            # Expecting payload like:
            # { "ts": "...Z", "machine_id": 1, "temperature": ..., "pressure": ..., "rpm": ..., "fault_code": ... }
            ts = payload.get("ts")
            machine_id = payload.get("machine_id")
            temperature = payload.get("temperature")
            pressure = payload.get("pressure")
            rpm = payload.get("rpm")
            fault_code = payload.get("fault_code")

            insert_sql = """
                INSERT INTO bronze_machine_events
                    (ts, machine_id, temperature, pressure, rpm, fault_code, raw_event)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
            """

            try:
                with conn.cursor() as cur:
                    cur.execute(
                        insert_sql,
                        (ts, machine_id, temperature, pressure, rpm, fault_code, Json(payload)),
                    )
                conn.commit()
                logger.info(f"Wrote event to bronze_machine_events: {payload}")
            except Exception as e:
                conn.rollback()
                logger.error(f"Failed to insert into Postgres: {e}")
                # optional: sleep a bit to avoid hot loop on DB errors
                time.sleep(1.0)

    except KeyboardInterrupt:
        logger.info("Shutting down bronze consumer...")
    finally:
        consumer.close()
        conn.close()


if __name__ == "__main__":
    main()
