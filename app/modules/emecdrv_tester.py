import logging
import time
from canopen import BaseNode402, RemoteNode, LocalNode

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView, QTableWidget
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QCursor

logger = logging.getLogger(__name__)

# EMECDRV SPECIFIC

MIN_TARGET_POSITION = 0  # 0% LIFT POSITION
MAX_TARGET_POSITION = 100  # 100% LIFT POSITION

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

    def __init__(self,
                 node: BaseNode402,
                 min_movement: int = 35,  # default for Lift
                 max_movement: int = 45  # default for Lift
                 ):
        super().__init__()

        self.node = node

        self.moving_time = 0
        self.elapsed_time = 0
        self.reached_status_timer = 0
        self.test_error_message = None

        # define min and max movement time
        self.min_movement = min_movement
        self.max_movement = max_movement

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
        self.timeout.connect(self.timeout_timer)

        logger.debug(f"EMECDrvTester created with node_id: {node.id}")

        self.initialised.emit()

    @property
    def ccw_movements(self):
        try:
            return self.node.sdo[0x2000][1].raw
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
            return self.node.sdo[OD_CURRENT_ACTUAL_VALUE].raw
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

    def get_elapsed_time(self) -> int:
        return self.elapsed_time

    @property
    def status(self) -> str:
        state = "Unknown"
        try:
            state = self.node.state
        except Exception as e:
            logger.debug(f'Error reading status: {e}')
            return "Error 0"

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

    def timeout_timer(self):
        self.elapsed_time = self.elapsed_time + 1
        self.test_timer_timeout.emit()

        try:
            if self.node.sdo[OD_STATUS_WORD].raw & STATUS_TARGET_REACHED or \
                    (self.actual_position < (self.node.sdo[OD_TARGET_POSITION].raw + 4) and \
                    self.actual_position > (self.node.sdo[OD_TARGET_POSITION].raw - 4)):
                if self.actual_position < (MAX_TARGET_POSITION - 50):
                    self.node.sdo[OD_TARGET_POSITION].raw = MAX_TARGET_POSITION
                else:
                    self.node.sdo[OD_TARGET_POSITION].raw = MIN_TARGET_POSITION

                self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_START_MOVEMENT_ORDER
                self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw | CONTROL_START_MOVEMENT_ORDER

                self.reached_status_timer = self.reached_status_timer + 1

                # control min movement time
                if self.moving_time < self.min_movement < self.elapsed_time:
                    self.test_error_message = f"Movement time under limit of {self.min_movement}s"
                    self.stop_test()  # Stop if timeout error

                if self.reached_status_timer > 10:
                    self.test_error_message = f"Driver always in reached status"
                    self.stop_test()  # Stop if timeout error

                self.moving_time = 0  # Reset timer when reaching target position

            else:
                # Control max movement time
                if self.moving_time > self.max_movement:
                    self.test_error_message = f"Movement timeout exceeded limit of {self.max_movement}s"
                    self.stop_test()  # Stop if timeout error

                    logger.debug("Error due to moving time exceeded")

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
