import json
import logging
import asyncio

import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

logger = logging.getLogger(__name__)


async def read_coils(client, start_address, length, slave_id=1):
    """
    Read coils from the modbus client (code 1)
    :param client:
    :param start_address:
    :param length:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.read_coils(start_address, length, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error reading coils")

    return rr.bits


async def read_discrete_inputs(client, start_address, length, slave_id=1):
    """
    Read discrete inputs from the modbus client (code 2)
    :param client:
    :param start_address:
    :param length:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.read_discrete_inputs(start_address, length, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error reading discrete inputs")

    return rr.bits


async def read_holding_registers(client, start_address, length, slave_id=1):
    """
    Read holding registers from the modbus client (code 3)
    :param client:
    :param start_address:
    :param length:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.read_holding_registers(start_address, length, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error reading coils from modbus")

    return rr.registers


async def read_input_registers(client, start_address, length, slave_id=1):
    """
    Read input registers from the modbus client (code 4)
    :param client:
    :param start_address:
    :param length:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.read_input_registers(start_address, length, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error reading input registers")

    return rr.registers


async def write_coil(client, start_address, value, slave_id=1):
    """
    Write a single coil to the modbus client (code 5)
    :param client:
    :param start_address:
    :param value:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.write_coil(start_address, value, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error writing coil")

    return rr.bits


async def write_register(client, start_address: int, value: int, slave_id: int = 1):
    """
    Write a single register to the modbus client (code 6)
    :param client:
    :param start_address:
    :param value:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.write_register(start_address, value, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error writing register")

    return rr.registers


async def write_coils(client, start_address: int, values: list[bool], slave_id: int = 1):
    """
    Write multiple coils to the modbus client (code 15)
    :param client:
    :param start_address:
    :param values:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.write_coils(start_address, values, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error writing coils")

    return rr.bits



async def write_registers(client, start_address: int, values: list[int], slave_id: int = 1):
    """
    Write multiple registers to the modbus client (code 16)
    :param client:
    :param start_address:
    :param values:
    :param slave_id:
    :return:
    """
    try:
        rr = await client.write_registers(start_address, values, slave=slave_id)
    except ModbusException as exc:
        logger.error(f"ERROR: exception in pymodbus {exc}")
        raise exc
    if rr.isError():
        logger.error("ERROR: pymodbus returned an error!")
        raise ModbusException("Error writing registers")

    return rr.registers


class ModbusClientWrapper:
    def __init__(self):
        self.client = None

        pymodbus_apply_logging_config("ERROR")

    async def init(self, comm, **kwargs):

        if comm == "tcp":
            host = kwargs.get("host", "localhost")
            port = kwargs.get("port", 5020)
            framer = kwargs.get("framer", FramerType.SOCKET)

            client = ModbusClient.AsyncModbusTcpClient(
                host,
                port=port,
                framer=framer,
                # timeout=10,
                # retries=3,
                # source_address=("localhost", 0),
            )
        elif comm == "udp":
            host = kwargs.get("host", "localhost")
            port = kwargs.get("port", 502)
            framer = kwargs.get("framer", FramerType.SOCKET)

            client = ModbusClient.AsyncModbusUdpClient(
                host,
                port=port,
                framer=framer,
                # timeout=10,
                # retries=3,
                # source_address=None,
            )
        elif comm == "serial":
            port = kwargs.get("port", "/dev/ttyUSB0")
            framer = kwargs.get("framer", FramerType.RTU)
            baud = kwargs.get("baudrate", 9600)
            bytesize = kwargs.get("bytesize", 8)
            parity = kwargs.get("parity", "N")
            stopbits = kwargs.get("stopbits", 1)

            client = ModbusClient.AsyncModbusSerialClient(
                port,
                framer=framer,
                # timeout=10,
                # retries=3,
                baudrate=baud,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits,
                # handle_local_echo=False,
            )
        else:
            print(f"Unknown client {comm} selected")
            return False

        await client.connect()
        self.client = client

        return client.connected


def find_register_by_name(registers_data, name):
    for register in registers_data:
        if register['name'] == name:
            return register
    return None


class ModbusManager:
    def __init__(self):
        self.register_map = None

        logger.info("Init Modbus clients")
        self.wrapper = ModbusClientWrapper()

    @property
    def status(self):
        return self.wrapper.client.connected

    async def init_modbus_client(self, cfg: dict):
        cfg['status'] = await self.wrapper.init(**cfg)  # Init Modbus clients

        register_map_path = cfg.get("register_map", None)  # Load register map
        if register_map_path is not None:
            with open(register_map_path, "r") as f:
                self.register_map = json.load(f)

    async def read_register(self, register_name: str):

        registers_data = (self.register_map.get("io_registers", []) +
                          self.register_map.get("system_registers", []))  # Get registers data

        register_info = find_register_by_name(registers_data, register_name)  # Find register by name
        if not register_info:
            print(f"Register {register_name} not found")
            return

        # Get register info
        start_address = register_info["start_address"]
        length = register_info["length"]
        function_code = register_info["function_code"]

        try:
            if function_code == "01":  # Read Coil
                result = await read_coils(self.wrapper.client, start_address, length)
            elif function_code == "02":  # Read Discrete Inputs
                result = await read_discrete_inputs(self.wrapper.client, start_address, length)
            elif function_code == "03":  # Read Holding Registers
                result = await read_holding_registers(self.wrapper.client, start_address, length)
            elif function_code == "04":  # Read Input Registers
                result = await read_input_registers(self.wrapper.client, start_address, length)
            else:
                print(f"Unsupported function code: {function_code}")
                return None

            return result

        except ModbusException as e:
            print(f"Modbus Error: {e}")
            return None

    async def write_register(self, register_name: str, value):

        registers_data = (self.register_map.get("io_registers", []) +
                          self.register_map.get("system_registers", []))  # Get registers data

        register_info = find_register_by_name(registers_data, register_name)  # Find register by name
        if not register_info:
            print(f"Register {register_name} not found")
            return

        # Get register info
        start_address = register_info["start_address"]
        function_code = register_info["function_code"]

        try:
            if function_code == "01" or function_code == "02":  # Write Coil or Coils
                if isinstance(value, list):
                    result = await write_coils(self.wrapper.client, start_address, value)
                else:
                    result = await write_coil(self.wrapper.client, start_address, value)
            elif function_code == "03" or function_code == "04":  # Write Holding Register or Registers
                if isinstance(value, list):
                    result = await write_registers(self.wrapper.client, start_address, value)
                else:
                    result = await write_register(self.wrapper.client, start_address, value)
            else:
                print(f"Unsupported function code for writing: {function_code}")
                return None

            return result

        except ModbusException as e:
            print(f"Modbus Error: {e}")
            return None
