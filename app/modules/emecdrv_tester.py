import logging
import time
from canopen import BaseNode402, RemoteNode, LocalNode

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView, QTableWidget
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QCursor

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
MIN_MOVEMENT_TIME_LIFT = 28
MAX_MOVEMENT_TIME_LIFT = 40
MIN_MOVEMENT_TIME_SLEWING = 130
MAX_MOVEMENT_TIME_SLEWING = 155

OD_MANUFACTURER_DEVICE_NAME = 0x1008
OD_MANUFACTURER_HARDWARE_VERSION = 0x1009
OD_MANUFACTURER_SOFTWARE_VERSION = 0x100A

OD_MODES_OF_OPERATION = 0x6060
OD_POSITION_ACTUAL_VALUE = 0x6064
OD_MAX_CURRENT = 0x6073
OD_MOTOR_RATED_CURRENT = 0x6075
OD_CURRENT_ACTUAL_VALUE = 0x6078
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


class EMECDrvTester(QTimer):

    initialised = pyqtSignal()
    started = pyqtSignal()
    stopped = pyqtSignal()
    failure = pyqtSignal()
    cycle = pyqtSignal()

    test_timer_timeout = pyqtSignal()

    def __init__(self, node: BaseNode402):
        super().__init__()

        self.node = node

        self.moving_time = 0
        self.elapsed_time = 0
        self.reached_status_timer = 0
        self.test_error_message = None

        self.min_target = MIN_TARGET_POSITION_LIFT,  # default for Lift
        self.max_target = MAX_TARGET_POSITION_LIFT  # default for Lift

        # int a value that cannot be min or max target
        self.target_temp = (MAX_TARGET_POSITION_LIFT - MIN_TARGET_POSITION_LIFT)/2

        self.tolerance = 10

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

            # define min and max movement time
            self.min_time = MIN_MOVEMENT_TIME_LIFT
            self.max_time = MAX_MOVEMENT_TIME_LIFT
            
            self.min_target = MIN_TARGET_POSITION_LIFT
            self.max_target = MAX_TARGET_POSITION_LIFT

        elif node.id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            self.timeout.connect(self.timeout_test)

            # define min and max movement time
            self.min_time = MIN_MOVEMENT_TIME_SLEWING  # minimum movement time in seconds
            self.max_time = MAX_MOVEMENT_TIME_SLEWING  # maximum movement time in seconds

            self.min_target = MIN_TARGET_POSITION_SLEWING
            self.max_target = MAX_TARGET_POSITION_SLEWING

            self.tolerance = 100

        logger.debug(f"EMECDrvTester created with node_id: {node.id}")
        logger.debug(f'min_movement: {self.min_time}, max_movement: {self.max_time}')

        self.initialised.emit()

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
    def min_time(self):
        """
        Minimum time that need to pass during a movement
        :return:
        """
        return self._min_time

    @min_time.setter
    def min_time(self, min_t: int):
        self._min_time = min_t

    @property
    def max_time(self):
        """
        Maximum time that can pass during a movement
        :return:
        """
        return self._max_time

    @max_time.setter
    def max_time(self, max_t: int):
        self._max_time = max_t

    @property
    def ccw_movements(self):
        """
        CCW movements red from CANOpen register
        :return:
        """
        try:
            return self.node.sdo[0x2000][1].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def accumulative_operating_time(self):
        try:
            return self.node.sdo[0x2000][0].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def device_temp(self):
        try:
            return self.node.sdo[0x2001][0].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def max_device_temp(self):
        try:
            return self.node.sdo[0x2001][1].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def cw_movements(self):
        try:
            return self.node.sdo[0x2000][2].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def actual_position(self):
        try:
            return self.node.sdo[OD_POSITION_ACTUAL_VALUE].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def target_position(self):
        try:
            return self.node.sdo[OD_TARGET_POSITION].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def max_current(self):
        try:
            return self.node.sdo[OD_MAX_CURRENT].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def rated_current(self):
        try:
            return self.node.sdo[OD_MOTOR_RATED_CURRENT].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def current_actual_value(self):
        try:
            return self.node.sdo[OD_CURRENT_ACTUAL_VALUE].raw * 4.5  # factor 4,5x
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def control_word(self):
        try:
            return self.node.sdo[OD_CONTROL_WORD].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def status_word(self):
        try:
            return self.node.sdo[OD_STATUS_WORD].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def manufacturer_device_name(self):
        """
        Return's manufacturer device name red from canopen registers
        :return:
        """
        try:
            return self.node.sdo[OD_MANUFACTURER_DEVICE_NAME].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def manufacturer_hardware_version(self):
        """
        Return's manufacturer hardware version red from canopen registers
        :return:
        """
        try:
            return self.node.sdo[OD_MANUFACTURER_HARDWARE_VERSION].raw
        except Exception as e:
            logger.debug(e)
            return 0

    @property
    def manufacturer_software_version(self):
        """
        Return's manufacturer software version red from canopen registers
        :return:
        """
        try:
            return self.node.sdo[OD_MANUFACTURER_SOFTWARE_VERSION].raw
        except Exception as e:
            logger.debug(e)
            return 0

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
        state = "Unknown"
        try:
            state = self.node.state
        except Exception as e:
            logger.debug(f'Error reading status: {e}')
            self.stop_test()  # Stop the test if these error occurs
            return "Error reading status"

        if self.isActive():
            if state == 'OPERATION ENABLED':
                state = "Test running"
            elif state == 'FAULT':
                state = "Error"
        else:
            if state == 'SWITCHED ON':
                state = "Stopped"
            elif state == 'FAULT':
                state = "Error"

        if self.test_error_message is not None:
            state = self.test_error_message

        return state

    def timeout_test(self):
        self.elapsed_time = self.elapsed_time + 1
        self.test_timer_timeout.emit()

        try:
            if (self.max_target - self.tolerance) < self.actual_position < (self.max_target + self.tolerance):
                if self.target_temp != self.min_target:
                    # control min movement time
                    if self.moving_time < self.min_time < self.elapsed_time:
                        self.test_error_message = f"Movement ({self.moving_time}s) time under limit of {self.min_time}s"
                        self.stop_test()  # Stop if timeout error
                    else:
                        self.stop_movement()
                        self.target_temp = self.min_target
                        self.node.sdo[OD_TARGET_POSITION].raw = self.min_target
                        QTimer.singleShot(1500, self.start_movement)
                        self.moving_time = 0  # Reset timer when reaching target position

                self.reached_status_timer = self.reached_status_timer + 1

                if self.reached_status_timer > 10:
                    self.test_error_message = f"Driver always in reached status"
                    self.stop_test()  # Stop if timeout error

            elif (-self.min_target - self.tolerance) < self.actual_position < (-self.min_target + self.tolerance):
                if self.target_temp != self.max_target:
                    # control min movement time
                    if self.moving_time < self.min_time < self.elapsed_time:
                        self.test_error_message = f"Movement time ({self.moving_time}s) under limit of {self.min_time}s"
                        self.stop_test()  # Stop if timeout error
                    else:
                        self.stop_movement()
                        self.target_temp = self.max_target
                        self.node.sdo[OD_TARGET_POSITION].raw = self.max_target
                        QTimer.singleShot(1500, self.start_movement)
                        self.moving_time = 0  # Reset timer when reaching target position

                self.reached_status_timer = self.reached_status_timer + 1

                if self.reached_status_timer > 10:
                    self.test_error_message = f"Driver always in reached status"
                    self.stop_test()  # Stop if timeout error

            else:
                # Control max movement time
                if self.moving_time > self.max_time:
                    self.test_error_message = f"Movement time ({self.moving_time}s) exceeded limit of {self.max_time}s"
                    self.stop_test()  # Stop if timeout error

                    logger.debug("Movement time ({self.moving_time}s) exceeded limit of {self.max_movement}s")

                self.moving_time = self.moving_time + 1  # increment timer during movement
                self.reached_status_timer = 0  # reset timer if out of reached status

        except Exception as e:
            logger.debug(f'Exception during testing routine: {e}')
            self.stop()

    def start_test(self):
        if not self.isActive():
            try:
                self.moving_time = 0
                self.reached_status_timer = 0
                self.test_error_message = None

                # Init target first time to min

                mid = (self.max_target - self.min_target) / 2
                if self.node.sdo[OD_TARGET_POSITION].raw > mid:
                    self.node.sdo[OD_TARGET_POSITION].raw = self.max_target
                else:
                    self.node.sdo[OD_TARGET_POSITION].raw = self.min_target

                self.start_movement()
            except Exception as e:
                logger.debug(f"Error starting test: {e}")
                self.failure.emit()
                return

            self.start(1000)  # Start QTimer with Timeout period
            self.started.emit()
            logger.debug(f"Start Test on Node {self.node.id} on network {self.node.network}")

    def stop_test(self):
        # Clear Operating Enabled flag
        try:
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_ENABLE_OPERATION
        except Exception as e:
            self.failure.emit()
            logger.debug(f"Error during stopping test: {e}")

        self.moving_time = 0
        self.elapsed_time = 0
        self.reached_status_timer = 0

        self.stop()  # Stop QTimer
        self.stopped.emit()
        logger.debug(f"Stop Test on Node {self.node.id}")

    def start_movement(self):

        # Set Operating Enabled flag
        self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw | CONTROL_ENABLE_OPERATION

        # A rising flank starts a movement order
        self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_START_MOVEMENT_ORDER
        self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw | CONTROL_START_MOVEMENT_ORDER

    def stop_movement(self):

        self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_ENABLE_OPERATION


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
            self.failure.emit()
            logger.debug(f"Error during ack:  {e}")

        self.test_error_message = None

        self.initialised.emit()
