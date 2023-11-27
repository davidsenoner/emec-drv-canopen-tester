import logging
import time
from canopen import BaseNode402, RemoteNode, LocalNode
from canopen.emcy import EmcyError
from collections import deque
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView, QTableWidget
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QSettings, QTimer
from PyQt5.QtGui import QCursor

from app.modules.utils import compare_versions

logger = logging.getLogger(__name__)

# EMECDRV SPECIFIC

TITAN40_EMECDRV5_LIFT_NODE_ID = 0x0C
TITAN40_EMECDRV5_SLEWING_NODE_ID = 0x0D

#  TARGET POSITIONS FOR TESTING MOVEMENT (NOTE: CHANGE MIN/MAX TIME IF TARGET CHANGES)
MIN_TARGET_POSITION_LIFT = 0  # 0% LIFT POSITION
MAX_TARGET_POSITION_LIFT = 100  # 100% LIFT POSITION
MIN_TARGET_POSITION_SLEWING = -100  # NEGATIVE VALUE FOR CCW MOVEMENT
MAX_TARGET_POSITION_SLEWING = 1900  # POSITIVE VALUE FOR CW MOVEMENT

#  MIN AND MAX TIME FOR MOVEMENT
MIN_MOVEMENT_TIME_LIFT = 20
MAX_MOVEMENT_TIME_LIFT = 65
MAX_MOVEMENT_TIME_ABSOLUTE = 500

OD_MANUFACTURER_DEVICE_NAME = 0x1008
OD_MANUFACTURER_HARDWARE_VERSION = 0x1009
OD_MANUFACTURER_SOFTWARE_VERSION = 0x100A
OD_DEVICE_ERROR_FLAGS = 0x2100

OD_MODES_OF_OPERATION = 0x6060
OD_POSITION_ACTUAL_VALUE = 0x6064
OD_MAX_CURRENT = 0x6073
OD_MOTOR_RATED_CURRENT = 0x6075
OD_CURRENT_ACTUAL_VALUE = 0x6078  # factor = OD_MOTOR_RATED_CURRENT / 1000
OD_DC_LINK_CIRCUIT_VOLTAGE = 0x6079  # Battery voltage
OD_TARGET_POSITION = 0x607A

OD_STATUS_WORD = 0x6041
OD_CONTROL_WORD = 0x6040

# STATUS WORD MASK
STATUS_READY_TO_SWITCH_ON = 0x0
STATUS_READY = 0x02
STATUS_OPERATION_ENABLED = 0x04
STATUS_FAULT = 0x08
STATUS_VOLTAGE_ENABLED = 0x10
STATUS_QUICK_STOP = 0x20
STATUS_SWITCH_ON_INHIBIT = 0x40
STATUS_WARNING_ACTIVE = 0x80
STATUS_START_FUNCTION = 0x100
STATUS_BUS_CONTROL_EN = 0x200
STATUS_TARGET_REACHED = 0x400
STATUS_INTERNAL_LIMIT_EXCEEDED = 0x800

# CONTROL WORD MASK
CONTROL_READY = 0x0
CONTROL_DISABLE_VOLTAGE = 0x02
CONTROL_QUICK_STOP = 0x04
CONTROL_ENABLE_OPERATION = 0x08
CONTROL_OPERATING_MODE_CUSTOM_1 = 0x10
CONTROL_START_MOVEMENT_ORDER = 0x10
CONTROL_OPERATING_MODE_CUSTOM_2 = 0x20
CONTROL_OPERATING_MODE_CUSTOM_3 = 0x40
CONTROL_ACK_ERROR = 0x80
CONTROL_STOP = 0x100

# Operating modes
PROFILE_POSITION_OPERATING_MODE = 0x01
VELOCITY_OPERATING_MODE = 0x02
PROFILE_VELOCITY_OPERATING_MODE = 0x03
PROFILE_TORQUE_OPERATING_MODE = 0x04
HOMING_OPERATING_MODE = 0x06

STOPPED = 0
CW = 1
CCW = 2


class EMECDrvTester(QTimer):
    test_timer_timeout = pyqtSignal()
    generate_label_signal = pyqtSignal()

    def __init__(self, node: BaseNode402):
        super().__init__()

        self.label_print_timeout = None
        self.not_moving_counter = 0  # counter for detection of no movement error
        self.wrong_movement_counter = 0  # counter for detection of wrong movement error
        self.actual_position_temp = None
        self.label_printed = False  # status bit True=Label already printed
        self.node = node

        self.moving_time = 0
        self.elapsed_time = 0
        self._max_error_current = 0
        self.test_error_message = None  # Message to show to screen
        self.moving_direction = None  # CCW, CW, STOPPED

        self.settings = QSettings("EMEC", "Tester")

        self.min_target = MIN_TARGET_POSITION_LIFT,  # default for Lift
        self.max_target = MAX_TARGET_POSITION_LIFT  # default for Lift

        # int a value that cannot be min or max target
        self.target_temp = (MAX_TARGET_POSITION_LIFT - MIN_TARGET_POSITION_LIFT) / 2

        self.tolerance = 0

        # Init FIFO for measured current values
        self.current_actual_value_fifo = deque(maxlen=20)

        # fill current value fifo with zero
        for _ in range(self.current_actual_value_fifo.maxlen):
            self.current_actual_value_fifo.append(0)

        # register emergency error callback that will stop with error message from canopen
        self.node.emcy.add_callback(self.emcy_callback)

        # Node initialisation
        node.nmt.state = 'OPERATIONAL'

        node.sdo[OD_MODES_OF_OPERATION].raw = PROFILE_POSITION_OPERATING_MODE  # “Profile Position” operating mode

        # Init Node state
        timeout = time.time() + 15
        node.state = 'READY TO SWITCH ON'
        while node.state != 'READY TO SWITCH ON':
            if time.time() > timeout:
                raise Exception('Timeout when trying to change state to READY TO SWITCH ON')
            time.sleep(0.001)

        timeout = time.time() + 15
        node.state = 'SWITCHED ON'
        while node.state != 'SWITCHED ON':
            if time.time() > timeout:
                raise Exception('Timeout when trying to change state to SWITCHED ON')
            time.sleep(0.001)

        timeout = time.time() + 15
        node.state = 'OPERATION ENABLED'
        while node.state != 'OPERATION ENABLED':
            if time.time() > timeout:
                raise Exception('Timeout when trying to change state to OPERATION ENABLED')
            time.sleep(0.001)

        # Connect Signals
        if node.id == TITAN40_EMECDRV5_LIFT_NODE_ID:
            self.timeout.connect(self.timeout_test)
            self.timeout.connect(self.timeout_stat)

            self.min_target = MIN_TARGET_POSITION_LIFT
            self.max_target = MAX_TARGET_POSITION_LIFT

            self.tolerance = 0

            self.max_error_current = int(self.settings.value("max_error_current_lift", 800))

        elif node.id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            self.timeout.connect(self.timeout_test)
            self.timeout.connect(self.timeout_stat)

            self.min_target = MIN_TARGET_POSITION_SLEWING
            self.max_target = MAX_TARGET_POSITION_SLEWING

            self.tolerance = 10

            self.max_error_current = int(self.settings.value("max_error_current_slewing", 600))

        logger.debug(f"EMECDrvTester created with node_id: {node.id}")

    @property
    def max_error_current(self):
        """
        Max current in mA for over-current detection
        :return: Current in mA
        """
        return self._max_error_current

    @max_error_current.setter
    def max_error_current(self, current: int):
        """
        Max current in mA for over-current detection
        :param current: Current limit in mA
        :return:
        """
        self._max_error_current = current

    @property
    def min_target(self):
        """
        Minimum target value that drive will reach during test process
        :return:
        """
        return self._min_target

    @min_target.setter
    def min_target(self, target: int):
        self._min_target = target

    @property
    def max_target(self):
        """
        Maximum target value that drive will reach during test process
        :return:
        """
        return self._max_target

    @max_target.setter
    def max_target(self, target: int):
        self._max_target = target

    @property
    def ccw_movements(self):
        return self.node.sdo[0x2000][1].raw

    @property
    def accumulative_operating_time(self):
        return self.node.sdo[0x2000][0].raw

    @property
    def device_temp(self):
        return self.node.sdo[0x2001][0].raw

    @property
    def max_device_temp(self):
        return self.node.sdo[0x2001][1].raw

    @property
    def cw_movements(self):
        return self.node.sdo[0x2000][2].raw

    @property
    def actual_position(self):
        return self.node.sdo[OD_POSITION_ACTUAL_VALUE].raw

    @property
    def target_position(self):
        return self.node.sdo[OD_TARGET_POSITION].raw

    @property
    def max_current(self):
        return self.node.sdo[OD_MAX_CURRENT].raw

    @property
    def rated_current(self):
        return self.node.sdo[OD_MOTOR_RATED_CURRENT].raw

    @property
    def current_actual_value(self):
        factor = float(self.rated_current) / 1000
        return self.node.sdo[OD_CURRENT_ACTUAL_VALUE].raw * factor  # added factor to raw value

    @property
    def current_mean_value(self):
        """
        Calculates mean value of last measured values during movement
        :return: Mean value
        """
        if len(self.current_actual_value_fifo) > 0:
            mean = np.mean(self.current_actual_value_fifo)
        else:
            mean = 0

        return mean

    @property
    def current_std_value(self):
        """
        Calculates standard deviation of last measured values during movement
        :return: Standard deviation
        """
        if len(self.current_actual_value_fifo) > 0:
            mean = np.std(self.current_actual_value_fifo)
        else:
            mean = 0

        return mean

    @property
    def dc_link_circuit_voltage(self):
        return self.node.sdo[OD_DC_LINK_CIRCUIT_VOLTAGE].raw

    @property
    def control_word(self):
        return self.node.sdo[OD_CONTROL_WORD].raw

    @property
    def status_word(self):
        return self.node.sdo[OD_STATUS_WORD].raw

    @property
    def manufacturer_device_name(self):
        """
        Return's manufacturer device name red from canopen registers
        :return:
        """
        return self.node.sdo[OD_MANUFACTURER_DEVICE_NAME].raw

    @property
    def manufacturer_hardware_version(self):
        """
        Return's manufacturer hardware version red from canopen registers
        :return:
        """
        return self.node.sdo[OD_MANUFACTURER_HARDWARE_VERSION].raw

    @property
    def manufacturer_software_version(self):
        """
        Return's manufacturer software version red from canopen registers
        :return:
        """
        return self.node.sdo[OD_MANUFACTURER_SOFTWARE_VERSION].raw

    def get_device_error_message(self) -> str:
        """
        Get Error message from CANOpen reading from register 0x2100

        Bit Description                 M/O
        0   Overcurrent error           M
        1   Overtemperature error       M
        2   Position controller error   M
        3   Following error             M

        :return: Concatenated error messages separated by ","
        """
        errors = []
        try:
            flag = self.node.sdo[OD_DEVICE_ERROR_FLAGS].raw
        except Exception as e:
            flag = 0
            logger.debug(e)

        # over-current error
        if flag & 0x01:
            errors.append("Overcurrent error")

        # over-temperature error
        if flag & 0x02:
            errors.append("Overtemperature error")

        # position controller error
        if flag & 0x04:
            errors.append("Position controller error")

        # following error
        if flag & 0x04:
            errors.append("Following error")

        error_msg = ""
        for error in errors:
            if len(error_msg):
                error_msg = error_msg + ", " + error
            else:
                error_msg = error

        return error_msg

    def emcy_callback(self, error: EmcyError):
        if error.code == 0x0000:
            self.stop_test(f"CANOpen error ({hex(error.code)}): Fault reset")
        if error.code == 0x2310:
            self.stop_test(f"CANOpen error ({hex(error.code)}): Overcurrent on motor driver")
        if error.code == 0x4310:
            self.stop_test(f"CANOpen error ({hex(error.code)}): Overtemperature error")
        if error.code == 0x8110:
            self.stop_test(f"CANOpen error ({hex(error.code)}): CAN controller overflow")
        if error.code == 0x8120:
            self.stop_test(f"CANOpen error ({hex(error.code)}): CAN error passive")
        if error.code == 0x8130:
            self.stop_test(f"CANOpen error ({hex(error.code)}): Life guard error or heartbeat error")
        if error.code == 0x8140:
            self.stop_test(f"CANOpen error ({hex(error.code)}): CAN controller recovered from bus-off state")
        if error.code == 0x8210:
            self.stop_test(f"CANOpen error ({hex(error.code)}): PDO not processed due to length error")
        if error.code == 0x8220:
            self.stop_test(f"CANOpen error ({hex(error.code)}): PDO length exceeded")
        if error.code == 0x8500:
            self.stop_test(f"CANOpen error ({hex(error.code)}): Position controller")
        if error.code == 0x8611:
            self.stop_test(f"CANOpen error ({hex(error.code)}): Following error")

    def get_software_version_ok(self) -> bool:
        # compare software version
        min_sw_version = 0

        # load min software version from settings depending on drive type
        if self.node.id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            min_sw_version = self.settings.value("min_sw_version_slewing", "v1.25")
        elif self.node.id == TITAN40_EMECDRV5_LIFT_NODE_ID:
            min_sw_version = self.settings.value("min_sw_version_lift", "v3.16")

        # compare min sw version with version from drive
        software_comparision = compare_versions(self.manufacturer_software_version, min_sw_version)

        return software_comparision >= 0

    def get_elapsed_time(self) -> int:
        """
        Return's elapsed time since test start
        :return:
        """
        return self.elapsed_time

    @property
    def status(self) -> str:
        """
        Generates a readable status message for UI table
        :return: Message string
        """

        # if there is already an error print message set previously
        if self.test_error_message is not None:
            return self.test_error_message
        else:
            state = self.node.state

            if self.isActive():
                if state == 'OPERATION ENABLED':
                    state = "Test running"
            else:
                if state == 'SWITCHED ON':
                    state = "Stopped"

            return state

    def goto_target_position(self, position: int):
        if self.actual_position > abs(position):  # abs() because slewing have negative value when turning CCW
            self.moving_direction = CCW
        elif self.actual_position < abs(position):
            self.moving_direction = CW
        else:
            self.moving_direction = STOPPED
            self.stop_test("Internal error: New target position same  as actual")

        self.stop_movement()  # stop movement
        self.node.sdo[OD_TARGET_POSITION].raw = self.target_temp = position
        # wait 1,5s until restart movement in opposite direction
        QTimer.singleShot(1500, self.start_movement)
        self.moving_time = 0  # Reset timer when reaching target position

    def timeout_stat(self):
        try:
            self.current_actual_value_fifo.append(self.current_actual_value)  # append actual current value to fifo
        except Exception as e:
            logger.debug(e)

    def timeout_test(self):
        """
        Timer is running if test have been started
        :return:
        """
        self.elapsed_time = self.elapsed_time + 1
        self.test_timer_timeout.emit()

        # detect max movement time exceeded
        if self.moving_time >= MAX_MOVEMENT_TIME_ABSOLUTE:
            self.stop_test(f"Max movement time of {MAX_MOVEMENT_TIME_ABSOLUTE}s exceeded!!")

        try:
            # check max current limit
            if self.current_mean_value > self.max_error_current:
                self.stop_test(f"Current limit exceeded (Imean= {self.current_mean_value} mA)")

            # check if error from CANOpen
            # if self.node.state == 'FAULT':
            # self.stop_test("CANOpen error: " + self.get_device_error_message())

            # check if drive is moving
            if self.actual_position_temp == self.actual_position:  # is not moving??
                self.not_moving_counter += 1
                logger.debug(f"Actual position not changing since {self.not_moving_counter}s")

                # if actual position doesn't change for more than 3s emit error
                if self.not_moving_counter >= 4:
                    self.stop_test(f"Drive is not moving since {self.not_moving_counter}s")

            else:  # drive is moving
                self.not_moving_counter = 0  # reset counter for detection "not moving" error

                if self.actual_position_temp is not None and self.actual_position is not None:
                    if self.actual_position_temp > self.actual_position:  # is drive moving CCW?
                        if self.moving_direction != CCW:  # if moving CCW but should CW
                            self.wrong_movement_counter += 1
                        else:
                            self.wrong_movement_counter = 0  # moving in correct direction
                    else:
                        if self.moving_direction != CW:  # if moving CW but should CCW
                            self.wrong_movement_counter += 1
                        else:
                            self.wrong_movement_counter = 0  # moving in correct direction

                # moving in wrong direction timer control
                if self.wrong_movement_counter >= 4:
                    self.stop_test(f"Drive is moving in wrong direction since {self.wrong_movement_counter}")

                self.actual_position_temp = self.actual_position  # update temp for actual position

            # max position reached condition
            if (abs(self.max_target) - self.tolerance) <= self.actual_position:
                if self.target_temp != self.min_target:
                    self.goto_target_position(self.min_target)  # go to the new position

            # min position reached condition
            elif self.actual_position <= (abs(self.min_target) + self.tolerance):
                if self.target_temp != self.max_target:
                    self.goto_target_position(self.max_target)  # go to the new position

            # drive is moving condition
            else:
                self.moving_time = self.moving_time + 1  # increment timer during movement

            # generate signal for printing/generating a label
            if not self.label_printed and self.elapsed_time > self.label_print_timeout:
                self.generate_label_signal.emit()
                self.label_printed = True

        except Exception as e:
            logger.debug(f'Exception during testing routine: {e}')
            self.stop()

    def start_test(self):
        if not self.isActive():
            try:
                # init vars to 0
                self.moving_time = 0
                self.not_moving_counter = 0  # counter for detection of no movement error
                self.wrong_movement_counter = 0  # counter for detection of wrong movement error
                self.test_error_message = None

                if self.node.id == TITAN40_EMECDRV5_LIFT_NODE_ID:
                    self.max_error_current = int(self.settings.value("max_error_current_lift", 800))

                elif self.node.id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
                    self.max_error_current = int(self.settings.value("max_error_current_slewing", 600))

                # at every start take setting of label printer timer
                self.label_print_timeout = int(self.settings.value("label_print_timer", 60))

                # Init target first time min or max depending on actual position
                mid = (self.max_target - self.min_target) / 2  # get mid-position

                if self.node.sdo[OD_TARGET_POSITION].raw > mid:
                    # move in CW direction
                    self.node.sdo[OD_TARGET_POSITION].raw = self.max_target
                    self.moving_direction = CW
                else:
                    # move in CCW direction
                    self.node.sdo[OD_TARGET_POSITION].raw = self.min_target
                    self.moving_direction = CCW

                self.start_movement()

                self.start(1000)  # Start QTimer with Timeout period
                logger.debug(f"Start Test Node: {self.node.id} on network {self.node.network}")

            except Exception as e:
                logger.debug(f"Error starting test: {e}")

    def stop_test(self, message: str = None):
        if message is not None:
            self.test_error_message = message
            logger.debug(f'Stop Test on Node {self.node.id} due to {message}')
        else:
            logger.debug(f'Stop Test on Node {self.node.id}')

        try:
            self.stop_movement()
        except Exception as e:
            logger.debug(f"Error sending stop command to device: {e}")

        self.moving_time = 0
        self.elapsed_time = 0
        self.not_moving_counter = 0

        # fill current value fifo with zero
        for _ in range(self.current_actual_value_fifo.maxlen):
            self.current_actual_value_fifo.append(0)

        self.stop()  # Stop QTimer

    def start_movement(self):

        try:
            # Set Operating Enabled flag
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw | CONTROL_ENABLE_OPERATION

            # A rising flank starts a movement order
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_START_MOVEMENT_ORDER
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw | CONTROL_START_MOVEMENT_ORDER
        except Exception as e:
            logger.debug(f'Cannot start movement: {e}')

    def stop_movement(self):
        try:
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_ENABLE_OPERATION
        except Exception as e:
            logger.debug(f'Cannot stop movement: {e}')

    def ack_error(self):
        """
        Acknowledge error toggling ack bit 0->1->0
        :return: None
        """
        try:
            control_word = self.node.sdo[OD_CONTROL_WORD].raw
            self.node.sdo[OD_CONTROL_WORD].raw = control_word & ~CONTROL_ACK_ERROR
            self.node.sdo[OD_CONTROL_WORD].raw = control_word | CONTROL_ACK_ERROR
            self.node.sdo[OD_CONTROL_WORD].raw = control_word & ~CONTROL_ACK_ERROR
        except Exception as e:
            logger.debug(f"Error during ack_error: {e}")

        self.test_error_message = None
