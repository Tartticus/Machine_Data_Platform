# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 14:19:54 2026

@author: matth
"""
import json
import logging
import time
from datetime import datetime
import os
from confluent_kafka import Producer
from pymodbus.client.sync import ModbusTcpClient  # note .sync here

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka_producer")

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "raw_machine_events"

MODBUS_HOST = os.getenv("MODBUS_HOST", "modbus-sim")
MODBUS_PORT = int(os.getenv("MODBUS_PORT", "5020"))

def create_kafka_producer() -> Producer:
    conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "client.id": "machine-modbus-producer",
    }
    return Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Delivery failed for record {msg.key()}: {err}")
    else:
        logger.debug(
            f"Record produced to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}"
        )


def main():
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    if not client.connect():
        logger.error(f"Could not connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT}")
        return

    producer = create_kafka_producer()

    logger.info(
        f"Starting Modbus → Kafka producer. "
        f"Modbus: {MODBUS_HOST}:{MODBUS_PORT}, Kafka: {KAFKA_BOOTSTRAP_SERVERS}, topic: {KAFKA_TOPIC}"
    )

    try:
        while True:
            # address=0, count=4, unit=1
            rr = client.read_holding_registers(0, 4, unit=1)

            if rr.isError():
                logger.error(f"Modbus read error: {rr}")
                time.sleep(1.0)
                continue

            temperature, pressure, rpm, fault_code = rr.registers

            event = {
                "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "machine_id": 1,
                "temperature": temperature,
                "pressure": pressure,
                "rpm": rpm,
                "fault_code": fault_code,
            }

            producer.produce(
                KAFKA_TOPIC,
                value=json.dumps(event).encode("utf-8"),
                on_delivery=delivery_report,
            )
            producer.poll(0)

            logger.info(f"Produced event: {event}")
            time.sleep(1.0)

    except KeyboardInterrupt:
        logger.info("Shutting down producer...")
    finally:
        producer.flush(10)
        client.close()


if __name__ == "__main__":
    main()
