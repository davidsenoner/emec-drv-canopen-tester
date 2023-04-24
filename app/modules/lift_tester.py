import logging

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
CONTROL_OPERATING_MODE_CUSTOM_2 = 0x20
CONTROL_OPERATING_MODE_CUSTOM_3 = 0x40
CONTROL_ACK_ERROR = 0x80
CONTROL_STOP = 0x100


class LiftTester(QTimer):
    def __init__(self,
                 node: BaseNode402
                 ):
        super().__init__()

        self.node = node
        self.timeout.connect(self.timeout_timer)

    @property
    def actual_position(self):
        return self.read_sdo(OD_POSITION_ACTUAL_VALUE)

    @property
    def max_current(self):
        return self.read_sdo(OD_MAX_CURRENT)

    @property
    def rated_current(self):
        return self.read_sdo(OD_MOTOR_RATED_CURRENT)

    @property
    def current_actual_value(self):
        return self.read_sdo(OD_CURRENT_ACTUAL_VALUE)

    @property
    def control_word(self):
        return self.read_sdo(OD_CONTROL_WORD)

    def disable_operation(self):
        self.write_sdo(OD_CONTROL_WORD, 0x0F & ~CONTROL_ENABLE_OPERATION)

    def enable_operation(self):
        self.write_sdo(OD_CONTROL_WORD, 0x0F | CONTROL_ENABLE_OPERATION)

    def write_sdo(self, index: int, value: int, subindex: int = None):
        try:
            if subindex is None:
                self.node.sdo[index].raw = value
            else:
                self.node.sdo[index][subindex].raw = value
        except Exception as e:
            logger.debug(f"Error writing SDO {e}")

    def read_sdo(self, index: int, subindex: int = None):
        try:
            if subindex is None:
                ret = self.node.sdo[index].raw
            else:
                ret = self.node.sdo[index][subindex].raw

            return ret
        except Exception as e:
            logger.debug(f"Error reading SDO {e}")
            return -1

    def timeout_timer(self):

        if self.read_sdo(OD_STATUS_WORD) & STATUS_TARGET_REACHED:
            if self.actual_position < (MAX_TARGET_POSITION - 5):
                self.move_to_position(MAX_TARGET_POSITION)
            else:
                self.move_to_position(MIN_TARGET_POSITION)
        else:
            pass

    def start_test(self):
        if not self.isActive():
            self.enable_operation()
            self.move_to_position(MAX_TARGET_POSITION)
            self.start(1000)
            logger.debug(f"Start Test on Node {self.node.id}")

    def stop_test(self):
        self.disable_operation()
        self.stop()
        logger.debug(f"Stop Test on Node {self.node.id}")

    def move_to_position(self, pos: int = 0):

        self.write_sdo(OD_TARGET_POSITION, pos)  # Set Target Position

        # Set rising edge for start movement order
        self.write_sdo(OD_CONTROL_WORD, 0x0F)
        self.write_sdo(OD_CONTROL_WORD, 0x1F)

    def ack_error(self):
        control_word = self.read_sdo(OD_CONTROL_WORD)
        self.write_sdo(OD_CONTROL_WORD, control_word | CONTROL_ACK_ERROR)


