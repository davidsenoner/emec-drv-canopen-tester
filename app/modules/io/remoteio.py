import logging
import asyncio
import threading
from app.modules.io import ModbusManager

logger = logging.getLogger(__name__)


def words_to_dword(h_word, l_word):
    return (h_word << 16) | l_word


def words_to_dwords(*words):
    """
    Converts a variable number of 16-bit words into a list of 32-bit integers.

    :param words: A variable number of 16-bit integer values.
    :return: A list of 32-bit integers corresponding to the input words.
    """
    dwords_list = []

    for i in range(0, len(words), 2):
        h_word = words[i]
        l_word = words[i + 1]
        dword = (h_word << 16) | l_word
        dwords_list.append(dword)

    return dwords_list


def dwords_to_words(*dwords):
    """
    Converts a variable number of 32-bit integers into a list of 16-bit words.

    :param dwords: A variable number of 32-bit integer values.
    :return: A list of 16-bit words corresponding to the input dwords.
    """
    words_list = []

    for dword in dwords:
        h_word = (dword >> 16) & 0xFFFF  # High word
        l_word = dword & 0xFFFF  # Low word
        words_list.extend([h_word, l_word])

    return words_list


def words_to_bytes(*words):
    """
    Converts a variable number of 16-bit words into a list of bytes.

    :param words: A variable number of 16-bit integer values.
    :return: A list of bytes corresponding to the input words.
    """
    bytes_list = []

    for word in words:
        byte1 = (word >> 8) & 0xFF  # High byte
        byte2 = word & 0xFF  # Low byte
        bytes_list.extend([byte1, byte2])

    return bytes_list


def words_to_string(words, byte_order='big'):
    """
    Converts a list of 16-bit values (words) into a string.

    :param words: List of 16-bit values.
    :param byte_order: 'big' for Big-Endian, 'little' for Little-Endian.
    :return: Decoded string.
    """
    bytes_list = []

    for word in words:
        if byte_order == 'big':
            # Extract the high byte (upper 8 bits) first
            high_byte = (word >> 8) & 0xFF
            # Extract the low byte (lower 8 bits)
            low_byte = word & 0xFF
        else:
            # For Little-Endian, extract the low byte first
            low_byte = word & 0xFF
            # Then extract the high byte
            high_byte = (word >> 8) & 0xFF

        # Add the two bytes to the list
        bytes_list.extend([high_byte, low_byte])

    # Convert the list of bytes into a bytes object
    byte_data = bytes(bytes_list)

    try:
        # Try decoding the bytes to a string using UTF-8
        result_string = byte_data.decode('utf-8').rstrip('\x00')
    except UnicodeDecodeError:
        # If decoding fails, fall back to Latin-1 decoding
        result_string = byte_data.decode('latin1').rstrip('\x00')

    return result_string


def dec_to_hex(dec_list):
    """
    Converts a list of decimal integers to a list of hexadecimal strings.

    :param dec_list: List of decimal integers.
    :return: List of hexadecimal strings.
    """
    # Convert each decimal number to a hexadecimal string
    hex_list = [hex(num)[2:].upper().zfill(2) for num in dec_list]

    return hex_list


def get_bit(word, bit_position):
    """
    Extracts the value of the bit at the specified position from a 16-bit word.

    :param word: A 16-bit integer value.
    :param bit_position: The position of the bit to extract (0-15, where 0 is the least significant bit).
    :return: The value of the specified bit (0 or 1).
    """
    if bit_position < 0 or bit_position > 15:
        raise ValueError("bit_position must be between 0 and 15")

    # Create a mask for the specified bit position
    mask = 1 << bit_position

    # Apply the mask and shift right to get the bit value (0 or 1)
    bit_value = (word & mask) >> bit_position

    return bit_value


class MoxaE1242:
    def __init__(self, ip: str = "192.168.127.254", port: int = 502, comm: str = "tcp", **kwargs):
        self._lanMac = None
        self._deviceName = None
        self._deviceUpTime = None
        self._firmwareVersion = None
        self._firmwareBuildDate = None
        self._lanIp = None
        self._modelName = None
        self._watchdogAlarmFlag = None

        self._AI_burnoutValue = None
        self._AI_burnoutValue_wr = None

        self._AI_mode = None
        self._AI_mode_wr = None

        self._AI_rawValue = None
        self._AI_rawValueMax = None
        self._AI_rawValueMin = None

        self._AI_resetMaxValue = None
        self._AI_resetMaxValue_wr = None

        self._AI_resetMinValue = None
        self._AI_resetMinValue_wr = None

        self._AI_scaledValue = None
        self._AI_scaledValueMax = None
        self._AI_scaledValueMin = None
        self._AI_status = None

        self._DI_counterOverflowFlag = None
        self._DI_counterOverflowFlag_wr = None

        self._DI_counterOverflowFlagClear = None
        self._DI_counterOverflowFlagClear_wr = None

        self._DI_counterReset = None
        self._DI_counterReset_wr = None

        self._DI_counterStatus = None
        self._DI_counterStatus_wr = None

        self._DI_counterValue = None
        self._DI_status = None
        self._DI_all_statusFromDI_00 = None

        self._DO_p2pSafeModeFlagClear = None
        self._DO_p2pSafeModeFlagClear_wr = None

        self._DO_p2pSafeModeFlag = None
        self._DO_p2pStatus = None

        self._DO_pulseCount = None
        self._DO_pulseCount_wr = None

        self._DO_pulseOffWidth = None
        self._DO_pulseOffWidth_wr = None

        self._DO_pulseOnWidth = None
        self._DO_pulseOnWidth_wr = None

        self._DO_pulseStatus = None
        self._DO_pulseStatus_wr = None

        self._DO_status = None
        self._DO_status_wr = None

        self._DO_all_statusFromDO_00 = None
        self._DO_all_statusFromDO_00_wr = None

        self._AI_channels_qty = 4
        self._DI_channels_qty = 4
        self._DO_channels_qty = 4
        self._DI_counter_channels_qty = 0
        self._DO_pulse_channels_qty = 0

        logger.info(f"Initializing Moxa E1242 with IP: {ip}")
        logger.info(f"Modbus port: {port}")
        logger.info(f"Modbus comm: {comm}")
        logger.info(f"Hardware configuration: AI channels: {self._AI_channels_qty}, DI channels: {self._DI_channels_qty}, "
                    f"DO channels: {self._DO_channels_qty}, DI counter channels: {self._DI_counter_channels_qty}")

        register_map = kwargs.get("register_map", "app/resources/register_map/e1242_mb_register_map.json")
        self.mb_cfg = {"comm": comm, "host": ip, "port": port, "register_map": register_map}
        self.modbus_manager = ModbusManager()  # Init Modbus manager

        threading.Thread(target=self.start).start()

    @property
    def status(self):
        return self.modbus_manager.status

    @property
    def AI_channels_qty(self):
        return self._AI_channels_qty

    @AI_channels_qty.setter
    def AI_channels_qty(self, value):
        self._AI_channels_qty = value

    @property
    def DI_channels_qty(self):
        return self._DI_channels_qty

    @DI_channels_qty.setter
    def DI_channels_qty(self, value):
        self._DI_channels_qty = value

    @property
    def DO_channels_qty(self):
        return self._DO_channels_qty

    @DO_channels_qty.setter
    def DO_channels_qty(self, value):
        self._DO_channels_qty = value

    @property
    def DI_counter_channels_qty(self):
        return self._DI_counter_channels_qty

    @DI_counter_channels_qty.setter
    def DI_counter_channels_qty(self, value):
        self._DI_counter_channels_qty = value

    @property
    def DO_pulse_channels_qty(self):
        return self._DO_pulse_channels_qty

    @DO_pulse_channels_qty.setter
    def DO_pulse_channels_qty(self, value):
        self._DO_pulse_channels_qty = value

    def start(self):
        asyncio.run(self.modbus_task())

    async def modbus_task(self):
        await self.modbus_manager.init_modbus_client(self.mb_cfg)
        await self.read_write_registers(0.5)

    async def read_write_registers(self, period=1.0):

        # once at the beginning
        self._modelName = await self.modbus_manager.read_register("modelName")
        self._deviceName = await self.modbus_manager.read_register("deviceName")
        self._firmwareVersion = await self.modbus_manager.read_register("firmwareVersion")
        self._firmwareBuildDate = await self.modbus_manager.read_register("firmwareBuildDate")
        self._lanIp = await self.modbus_manager.read_register("lanIp")
        self._lanMac = await self.modbus_manager.read_register("lanMac")
        self._watchdogAlarmFlag = await self.modbus_manager.read_register("watchdogAlarmFlag")

        # cyclic
        while True:
            # read system registers
            self._deviceUpTime = await self.modbus_manager.read_register("deviceUpTime")

            # read analog input registers
            self._AI_burnoutValue = await self.modbus_manager.read_register("AI_burnoutValue")
            self._AI_mode = await self.modbus_manager.read_register("AI_mode")
            self._AI_rawValue = await self.modbus_manager.read_register("AI_rawValue")
            self._AI_rawValueMax = await self.modbus_manager.read_register("AI_rawValueMax")
            self._AI_rawValueMin = await self.modbus_manager.read_register("AI_rawValueMin")
            # self._AI_resetMaxValue = await self.modbus_manager.read_register("AI_resetMaxValue")
            # self._AI_resetMinValue = await self.modbus_manager.read_register("AI_resetMinValue")
            self._AI_scaledValue = await self.modbus_manager.read_register("AI_scaledValue")
            self._AI_scaledValueMax = await self.modbus_manager.read_register("AI_scaledValueMax")
            self._AI_scaledValueMin = await self.modbus_manager.read_register("AI_scaledValueMin")
            self._AI_status = await self.modbus_manager.read_register("AI_status")

            # read digital input registers
            self._DI_counterOverflowFlag = await self.modbus_manager.read_register("DI_counterOverflowFlag")
            self._DI_counterOverflowFlagClear = await self.modbus_manager.read_register("DI_counterOverflowFlagClear")
            self._DI_counterReset = await self.modbus_manager.read_register("DI_counterReset")
            self._DI_counterStatus = await self.modbus_manager.read_register("DI_counterStatus")
            self._DI_counterValue = await self.modbus_manager.read_register("DI_counterValue")
            self._DI_status = await self.modbus_manager.read_register("DI_status")
            self._DI_all_statusFromDI_00 = await self.modbus_manager.read_register("DI_all_statusFromDI_00")

            # read digital output registers
            self._DO_p2pSafeModeFlagClear = await self.modbus_manager.read_register("DO_p2pSafeModeFlagClear")
            self._DO_p2pSafeModeFlag = await self.modbus_manager.read_register("DO_p2pSafeModeFlag")
            self._DO_p2pStatus = await self.modbus_manager.read_register("DO_p2pStatus")
            self._DO_pulseCount = await self.modbus_manager.read_register("DO_pulseCount")
            self._DO_pulseOffWidth = await self.modbus_manager.read_register("DO_pulseOffWidth")
            self._DO_pulseOnWidth = await self.modbus_manager.read_register("DO_pulseOnWidth")
            self._DO_pulseStatus = await self.modbus_manager.read_register("DO_pulseStatus")
            self._DO_status = await self.modbus_manager.read_register("DO_status")
            self._DO_all_statusFromDO_00 = await self.modbus_manager.read_register("DO_all_statusFromDO_00")

            # write registers
            if self._AI_burnoutValue_wr is not None:
                await self.modbus_manager.write_register("AI_burnoutValue", self._AI_burnoutValue_wr)
                self._AI_burnoutValue_wr = None

            if self._AI_mode_wr is not None:
                await self.modbus_manager.write_register("AI_mode", self._AI_mode_wr)
                self._AI_mode_wr = None

            if self._AI_resetMaxValue_wr is not None:
                await self.modbus_manager.write_register("AI_resetMaxValue", self._AI_resetMaxValue_wr)
                self._AI_resetMaxValue_wr = None

            if self._AI_resetMinValue_wr is not None:
                await self.modbus_manager.write_register("AI_resetMinValue", self._AI_resetMinValue_wr)
                self._AI_resetMinValue_wr = None

            if self._DI_counterOverflowFlag_wr is not None:
                await self.modbus_manager.write_register("DI_counterOverflowFlag", self._DI_counterOverflowFlag_wr)
                self._DI_counterOverflowFlag_wr = None

            if self._DI_counterOverflowFlagClear_wr is not None:
                await self.modbus_manager.write_register("DI_counterOverflowFlagClear",
                                                         self._DI_counterOverflowFlagClear_wr)
                self._DI_counterOverflowFlagClear_wr = None

            if self._DI_counterReset_wr is not None:
                await self.modbus_manager.write_register("DI_counterReset", self._DI_counterReset_wr)
                self._DI_counterReset_wr = None

            if self._DI_counterStatus_wr is not None:
                await self.modbus_manager.write_register("DI_counterStatus", self._DI_counterStatus_wr)
                self._DI_counterStatus_wr = None

            if self._DO_p2pSafeModeFlagClear_wr is not None:
                await self.modbus_manager.write_register("DO_p2pSafeModeFlagClear", self._DO_p2pSafeModeFlagClear_wr)
                self._DO_p2pSafeModeFlagClear_wr = None

            if self._DO_pulseCount_wr is not None:
                await self.modbus_manager.write_register("DO_pulseCount", self._DO_pulseCount_wr)
                self._DO_pulseCount_wr = None

            if self._DO_pulseOffWidth_wr is not None:
                await self.modbus_manager.write_register("DO_pulseOffWidth", self._DO_pulseOffWidth_wr)
                self._DO_pulseOffWidth_wr = None

            if self._DO_pulseOnWidth_wr is not None:
                await self.modbus_manager.write_register("DO_pulseOnWidth", self._DO_pulseOnWidth_wr)
                self._DO_pulseOnWidth_wr = None

            if self._DO_pulseStatus_wr is not None:
                await self.modbus_manager.write_register("DO_pulseStatus", self._DO_pulseStatus_wr)
                self._DO_pulseStatus_wr = None

            if self._DO_status_wr is not None:
                await self.modbus_manager.write_register("DO_status", self._DO_status_wr)
                self._DO_status_wr = None

            if self._DO_all_statusFromDO_00_wr is not None:
                await self.modbus_manager.write_register("DO_all_statusFromDO_00", self._DO_all_statusFromDO_00_wr)
                self._DO_all_statusFromDO_00_wr = None

            await asyncio.sleep(period)

    @property
    def device_name(self):
        return words_to_string(self._deviceName)

    @property
    def device_uptime(self):
        return words_to_dword(self._deviceUpTime[0], self._deviceUpTime[1])

    @property
    def firmware_version(self):
        numbers = words_to_bytes(*self._firmwareVersion)
        return f"V{numbers[0]}.{numbers[1]}.{numbers[2]}"

    @property
    def firmware_build_date(self):
        date = words_to_bytes(*self._firmwareBuildDate)
        return f"Build{date[0]:02}{date[1]:02}{date[2]:02}{date[3]:02}"

    @property
    def lan_ip(self):
        return words_to_bytes(*self._lanIp)

    @property
    def lan_mac(self):
        return dec_to_hex(words_to_bytes(*self._lanMac))

    @property
    def model_name(self):
        return words_to_string(self._modelName)

    @property
    def watchdog_alarm_flag(self):
        return self._watchdogAlarmFlag[0]

    def get_AI_burnout_value(self, channel=None):
        """
        Get the burnout value of the specified channel.
        :param channel: Channel number (1-4). If None, return the burnout value of all channels.
        :return:
        """
        dwords = words_to_dwords(*self._AI_burnoutValue)
        if channel is not None:
            return dwords[channel]
        return dwords

    def set_AI_burnout_value(self, channel, value):
        """
        Set the burnout value of the specified channel.
        :param channel: Channel number (1-4).
        :param value: Burnout value.
        """
        temp = self._AI_burnoutValue.copy()
        high_word, low_word = dwords_to_words(value)
        temp[channel * 2] = high_word
        temp[channel * 2 + 1] = low_word

        self._AI_burnoutValue_wr = temp

    def get_AI_mode(self, channel=None):
        """
        Get the AI mode of the specified channel.
        :param channel: Channel number (1-4). If None, return the mode of all channels.
        :return: 0: 0-10 V 1: 4-20mA 2: 0-20mA 4: 4-20mA (burnout)
        """
        if channel is not None:
            return self._AI_mode[channel]
        return self._AI_mode

    def set_AI_mode(self, channel, mode):
        """
        Set the AI mode of the specified channel.
        :param channel: Channel number (1-4).
        :param mode: 0: 0-10 V, 1: 4-20mA, 2: 0-20mA, 4: 4-20mA (burnout)
        """
        temp = self._AI_mode.copy()
        temp[channel] = mode

        self._AI_mode_wr = temp

    def get_AI_raw_value(self, channel=None):
        """
        Get the raw value of the specified channel.
        :param channel: Channel number (1-4). If None, return the raw value of all channels.
        :return: Raw value of the channel.
        """
        if channel is not None:
            return self._AI_rawValue[channel]
        return self._AI_rawValue

    def get_AI_raw_value_max(self, channel=None):
        """
        Get the maximum raw value of the specified channel.
        :param channel: Channel number (1-4). If None, return the maximum raw value of all channels.
        :return: Maximum raw value of the channel.
        """
        if channel is not None:
            return self._AI_rawValueMax[channel]
        return self._AI_rawValueMax

    def get_AI_raw_value_min(self, channel=None):
        """
        Get the minimum raw value of the specified channel.
        :param channel: Channel number (1-4). If None, return the minimum raw value of all channels.
        :return: Minimum raw value of the channel.
        """
        if channel is not None:
            return self._AI_rawValueMin[channel]
        return self._AI_rawValueMin

    def reset_AI_max_value(self):
        """
        Reset AI max value.
        """
        self._AI_resetMaxValue_wr = True

    def reset_AI_min_value(self):
        """
        Reset AI min value.
        """
        self._AI_resetMinValue_wr = True

    def get_AI_scaled_value(self, channel=None):
        """
        Get the scaled value of the specified channel.
        :param channel: Channel number (1-4). If None, return the scaled value of all channels.
        :return: Scaled value of the channel.
        """
        dwords = words_to_dwords(*self._AI_scaledValue)
        if channel is not None:
            return dwords[channel]
        return dwords

    def get_AI_scaled_value_max(self, channel=None):
        """
        Get the maximum scaled value of the specified channel.
        :param channel: Channel number (1-4). If None, return the maximum scaled value of all channels.
        :return: Maximum scaled value of the channel.
        """
        dwords = words_to_dwords(*self._AI_scaledValueMax)
        if channel is not None:
            return dwords[channel]
        return dwords

    def get_AI_scaled_value_min(self, channel=None):
        """
        Get the minimum scaled value of the specified channel.
        :param channel: Channel number (1-4). If None, return the minimum scaled value of all channels.
        :return: Minimum scaled value of the channel.
        """
        dwords = words_to_dwords(*self._AI_scaledValueMin)
        if channel is not None:
            return dwords[channel]
        return dwords

    def get_AI_status(self, channel=None):  # noqa
        """
        Get the status of the specified channel.
        :param channel: Channel number (1-4). If None, return the status of all channels.
        :return: Status of the channel. 0: normal, 1: burnout, 2: over range, 3: under range
        """
        if channel is not None:
            return self._AI_status[channel]
        return self._AI_status

    def get_DI_counter_overflow_flag(self, channel=None):
        """
        Get the counter overflow flag of the specified channel.
        :param channel: Channel number (1-4). If None, return the counter overflow flag of all channels.
        :return: Counter overflow flag of the channel. 0: Normal, 1: Overflow
        """
        if channel is not None:
            return self._DI_counterOverflowFlag[channel]
        return self._DI_counterOverflowFlag

    def get_DI_counter_overflow_flag_clear(self, channel=None):
        """
        Get the counter overflow flag clear of the specified channel.
        :param channel: Channel number (1-4). If None, return the counter overflow flag clear of all channels.
        :return: Counter overflow flag clear of the channel. 1: clear overflow flag
        """
        if channel is not None:
            return self._DI_counterOverflowFlagClear[channel]
        return self._DI_counterOverflowFlagClear

    def clear_DI_counter_overflow_flag(self):
        self._DI_counterOverflowFlagClear_wr = [True] * self._DI_counter_channels_qty

    def reset_DI_counter(self):
        """
        Reset the counter of existing counter channels.
        """
        self._DI_counterReset_wr = [True] * self._DI_counter_channels_qty

    def get_DI_counter_status(self, channel=None):
        """
        Get the counter status of the specified channel.
        :param channel: Channel number (1-4). If None, return the counter status of all channels.
        :return: Counter status of the channel. 0: STOP, 1: START
        """
        if channel is not None:
            return self._DI_counterStatus[channel]
        return self._DI_counterStatus

    def set_DI_counter_status(self, channel, status):
        """
        Set the counter status of the specified channel.
        :param channel: Channel number (1-4).
        :param status: Counter status of the channel. 0: STOP, 1: START
        """
        if channel >= self._DI_counter_channels_qty:
            raise ValueError(f"Channel number must be between 1 and {self._DI_counter_channels_qty}")

        temp = self._DI_counterStatus.copy()[0:self._DI_counter_channels_qty]
        temp[channel] = status

        self._DI_counterStatus_wr = temp

    def get_DI_counter_value(self, channel=None):
        """
        Get the counter value of the specified channel.
        :param channel: Channel number (1-4). If None, return the counter value of all channels.
        :return: Counter value of the channel.
        """
        dwords = words_to_dwords(*self._DI_counterValue)
        if channel is not None:
            return dwords[channel]
        return dwords

    def get_DI_status(self, channel=None):
        """
        Get the status of the specified channel.
        :param channel: Channel number (1-4). If None, return the status of all channels.
        :return: Status of the channel. 0: OFF, 1: ON
        """
        if channel is not None:
            return self._DI_status[channel]
        return self._DI_status

    def get_DI_all_status_from_DI_00(self):
        """
        Get the status of all digital inputs.
        :return: Status of all digital inputs.
        """
        return self._DI_all_statusFromDI_00

    def get_DO_p2p_safe_mode_flag(self, channel=None):
        """
        Get the point-to-point safe mode flag of the specified channel.
        :param channel: Channel number (1-4). If None, return the point-to-point safe mode flag of all channels.
        :return: Point-to-point safe mode flag of the channel. 0: OFF, 1: ON
        """
        if channel is not None:
            return self._DO_p2pSafeModeFlag[channel]
        return self._DO_p2pSafeModeFlag

    def get_DO_p2p_safe_mode_flag_clear(self, channel=None):
        """
        Get the point-to-point status of the specified channel.
        :param channel: Channel number (1-4). If None, return the point-to-point status of all channels.
        :return: Point-to-point status of the channel. 1: clear safe mode flag
        """
        if channel is not None:
            return self._DO_p2pSafeModeFlagClear[channel]
        return self._DO_p2pSafeModeFlagClear

    def clear_DO_p2p_safe_mode_flag(self, channel):
        """
        Clear the point-to-point safe mode flag of the specified channel.
        :param channel: Channel number (1-4).
        :return: None
        """
        if channel >= self.DO_pulse_channels_qty:
            raise ValueError(f"Channel number must be between 1 and {self.DO_pulse_channels_qty}")

        temp = [False] * self.DO_pulse_channels_qty
        temp[channel] = True
        self._DO_p2pSafeModeFlagClear_wr = temp

    def get_DO_p2p_status(self, channel=None):
        """
        Get the point-to-point status of the specified channel.
        :param channel: Channel number (1-4). If None, return the point-to-point status of all channels.
        :return: Point-to-point status of the channel. 0: OFF, 1: ON
        """
        if channel is not None:
            return self._DO_p2pStatus[channel]
        return self._DO_p2pStatus

    def get_DO_pulse_count(self, channel=None):
        """
        Get the pulse count of the specified channel.
        :param channel: Channel number (1-4). If None, return the pulse count of all channels.
        :return: Pulse count of the channel.
        """
        if channel is not None:
            return self._DO_pulseCount[channel]
        return self._DO_pulseCount

    def set_DO_pulse_count(self, channel, count):
        """
        Set the pulse count of the specified channel.
        :param channel: Channel number (1-4).
        :param count: Pulse count of the channel.
        """
        if channel >= self.DO_pulse_channels_qty:
            raise ValueError(f"Channel number must be between 1 and {self.DO_pulse_channels_qty}")

        temp = self._DO_pulseCount.copy()[0:self.DO_pulse_channels_qty]
        temp[channel] = count

        self._DO_pulseCount_wr = temp

    def get_DO_pulse_off_width(self, channel=None):
        """
        Get the pulse off width of the specified channel.
        :param channel: Channel number (1-4). If None, return the pulse off width of all channels.
        :return: Pulse off width of the channel. unit: 1 ms
        """
        if channel is not None:
            return self._DO_pulseOffWidth[channel]
        return self._DO_pulseOffWidth

    def set_DO_pulse_off_width(self, channel, width):
        """
        Set the pulse off width of the specified channel.
        :param channel: Channel number (1-4).
        :param width: Pulse off width of the channel. unit: 1 ms
        """
        if channel >= self.DO_pulse_channels_qty:
            raise ValueError(f"Channel number must be between 1 and {self.DO_pulse_channels_qty}")

        temp = self._DO_pulseOffWidth.copy()[0:self.DO_pulse_channels_qty]
        temp[channel] = width

        self._DO_pulseOffWidth_wr = temp

    def get_DO_pulse_on_width(self, channel=None):
        """
        Get the pulse on width of the specified channel.
        :param channel: Channel number (1-4). If None, return the pulse on width of all channels.
        :return: unit: 1 ms
        """
        if channel is not None:
            return self._DO_pulseOnWidth[channel]
        return self._DO_pulseOnWidth

    def set_DO_pulse_on_width(self, channel, width):
        """
        Set the pulse on width of the specified channel.
        :param channel: Channel number (1-4).
        :param width: Pulse on width of the channel. unit: 1 ms
        """
        if channel >= self.DO_pulse_channels_qty:
            raise ValueError(f"Channel number must be between 1 and {self.DO_pulse_channels_qty}")

        temp = self._DO_pulseOnWidth.copy()[0:self.DO_pulse_channels_qty]
        temp[channel] = width

        self._DO_pulseOnWidth_wr = temp

    def get_DO_pulse_status(self, channel=None):
        """
        Get the pulse status of the specified channel.
        :param channel: Channel number (1-4). If None, return the pulse status of all channels.
        :return: Pulse status of the channel. 0: STOP, 1: START
        """
        if channel is not None:
            return self._DO_pulseStatus[channel]
        return self._DO_pulseStatus

    def set_DO_pulse_status(self, channel, status):
        """
        Set the pulse status of the specified channel.
        :param channel: Channel number (1-4).
        :param status: Pulse status of the channel. 0: STOP, 1: START
        """
        if channel >= self.DO_pulse_channels_qty:
            raise ValueError(f"Channel number must be between 1 and {self.DO_pulse_channels_qty}")

        temp = self._DO_pulseStatus.copy()[0:self.DO_pulse_channels_qty]
        temp[channel] = status

        self._DO_pulseStatus_wr = temp

    def get_DO_status(self, channel=None):
        """
        Get the status of the specified channel.
        :param channel: Channel number (1-4). If None, return the status of all channels.
        :return: Status of the channel. 0: OFF, 1: ON
        """
        if channel is not None:
            return self._DO_status[channel]
        return self._DO_status

    def set_DO_status(self, channel, status):
        """
        Set the status of the specified channel.
        :param channel: Channel number (1-4).
        :param status: Status of the channel. 0: OFF, 1: ON
        """
        temp = self._DO_status.copy()[0:self._DO_channels_qty]
        temp[channel] = status

        self._DO_status_wr = temp

    def get_DO_all_status_from_DO_00(self):
        """
        Get the status of all digital outputs.
        :return: Status of all digital outputs.
        """
        return self._DO_all_statusFromDO_00

    def set_DO_all_status_from_DO_00(self, status):
        """
        Set the status of all digital outputs.
        :param status: Status of all digital outputs.
        """
        self._DO_all_statusFromDO_00_wr = status
