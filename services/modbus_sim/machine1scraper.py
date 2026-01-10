# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 12:59:26 2026

@author: matth
"""

import logging
import random
import threading
import time

from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
from pymodbus.server.sync import StartTcpServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("modbus_sim")


def create_context():
    # 10 holding registers total
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 10),
        co=ModbusSequentialDataBlock(0, [0] * 10),
        hr=ModbusSequentialDataBlock(0, [0] * 10),
        ir=ModbusSequentialDataBlock(0, [0] * 10),
    )
    context = ModbusServerContext(slaves=store, single=True)
    return context


def update_registers_forever(context, interval_seconds=1.0):
    slave_id = 0x01  # unit ID

    while True:
        temperature = int(random.uniform(200, 350))
        pressure = int(random.uniform(900, 1100))
        rpm = int(random.uniform(800, 2000))
        fault_code = random.choices([0, 1, 2], weights=[0.9, 0.08, 0.02])[0]

        regs = [temperature, pressure, rpm, fault_code]

        # 3 = holding registers
        context[slave_id].setValues(3, 0, regs)

        logger.info(
            "Updated regs: temp=%s pressure=%s rpm=%s fault=%s",
            temperature, pressure, rpm, fault_code,
        )
        time.sleep(interval_seconds)


def main():
    host = "0.0.0.0"
    port = 5020

    context = create_context()

    t = threading.Thread(target=update_registers_forever, args=(context,), daemon=True)
    t.start()

    logger.info("Starting Modbus TCP simulator on %s:%s", host, port)
    logger.info("Registers 0–3 = temperature, pressure, rpm, fault_code")

    StartTcpServer(context, address=(host, port))


if __name__ == "__main__":
    main()
