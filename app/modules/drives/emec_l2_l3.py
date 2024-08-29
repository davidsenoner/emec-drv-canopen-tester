import time
import logging

from PyQt5.QtCore import pyqtSignal, QSettings, QTimer

from app.modules.io.remoteio import MoxaE1242
from app.modules.drives.defines import MAX_MOVEMENT_TIME_ABSOLUTE_SLEWING
from app.widgets.dialogs.add_serial_number import AddSNDialog
from app.modules.drives.defines import IO_DRIVE_SLEWING_ID
from app.modules.test_report import Label

logger = logging.getLogger(__name__)

STOPPED = 0
CW = 1
CCW = 2


class EmecL2L3IO:
    def __init__(self, remote_io: MoxaE1242, enable_pin: int = 0, direction_pin: int = 1, angle_pin: int = 0,  **kwargs):
        self._remote_io = remote_io
        self._enable_pin = enable_pin
        self._direction_pin = direction_pin
        self._angle_pin = angle_pin

        self._min_voltage = 0
        self._max_voltage = 10
        self._min_angle_raw = 0
        self._max_angle_raw = 0xfffe

        self._voltage_at_min_angle = kwargs.get("voltage_at_min_angle", 0.5)
        self._voltage_at_max_angle = kwargs.get("voltage_at_max_angle", 4.5)
        self._en_active_high = kwargs.get("en_active_high", True)
        self._dir_active_high = kwargs.get("dir_active_high", True)
        self._min_angle = 0
        self._max_angle = 359

    def __repr__(self):
        return f"EmecL2L3IO(EN:{self._enable_pin}, DIR:{self._direction_pin}, ANGLE:{self._angle_pin})"

    @property
    def min_angle(self):
        return self._min_angle

    @min_angle.setter
    def min_angle(self, value):
        self._min_angle = value

    @property
    def max_angle(self):
        return self._max_angle

    @max_angle.setter
    def max_angle(self, value):
        self._max_angle = value

    @property
    def min_voltage_at_0_deg(self):
        return self._voltage_at_min_angle

    @min_voltage_at_0_deg.setter
    def min_voltage_at_0_deg(self, value):
        self._voltage_at_min_angle = value

    @property
    def max_voltage_at_360_deg(self):
        return self._voltage_at_max_angle

    @max_voltage_at_360_deg.setter
    def max_voltage_at_360_deg(self, value):
        self._voltage_at_max_angle = value

    def set_direction(self, direction: bool):
        """
        Set the direction of the motor
        :param direction: False for CW, True for CCW
        :return:
        """
        if self._dir_active_high:
            self._remote_io.set_DO_status(self._direction_pin, direction)
        else:
            self._remote_io.set_DO_status(self._direction_pin, not direction)

        time.sleep(0.1)

    def set_enable(self, enable: bool):
        """
        Enable or disable the motor
        :param enable: True to enable, False to disable
        :return:
        """
        if self._en_active_high:
            self._remote_io.set_DO_status(self._enable_pin, enable)
        else:
            self._remote_io.set_DO_status(self._enable_pin, not enable)  # inverted logic since E1242 DO sink type

    def get_AI_voltage(self) -> float:
        """
        Get the voltage on AI pin
        :return: float - Angle in degrees
        """
        raw_value = self._remote_io.get_AI_raw_value(self._angle_pin)

        return self._min_voltage + (self._max_voltage - self._min_voltage) * (raw_value - self._min_angle_raw) / (self._max_angle_raw - self._min_angle_raw)

    def get_actual_angle(self) -> float:
        """
        Get the angle of the motor
        :return: float - Angle in degrees
        """
        voltage = self.get_AI_voltage()
        return self._min_angle + (self._max_angle - self._min_angle) * (voltage - self._voltage_at_min_angle) / (self._voltage_at_max_angle - self._voltage_at_min_angle)

    def get_ai_voltage_range(self, tolerance=0.1):
        """
        Get the range of the AI voltage
        :return: int - 0 for below min, 1 for in range, 2 for above max
        """
        if self.get_AI_voltage() < self.min_voltage_at_0_deg - tolerance:
            return 0
        elif self.get_AI_voltage() > self.max_voltage_at_360_deg + tolerance:
            return 2
        else:
            return 1


class EMECL2L3Drive(QTimer):
    on_label_ready = pyqtSignal(Label)
    on_print_label = pyqtSignal(int)

    def __init__(self, io: EmecL2L3IO):
        super().__init__()

        self._serial_number = 0
        self._customer = ""
        self._comment = ""

        self.drive_removed = True
        self.label_ready = False
        self.moving_direction = None
        self.label_print_timeout = None
        self.io = io
        self.moving_time = 0
        self.elapsed_time = 0
        self.elapsed_time_2_temp = 0
        self.cw_movements = 0
        self.ccw_movements = 0
        self.actual_angle_temp = 0
        self.not_moving_counter = 0  # counter for detection of no movement error
        self.wrong_movement_counter = 0  # counter for detection of wrong movement error
        self.test_error_message = None  # Message to show to screen
        self.drive_present_since = 0

        self.settings = QSettings("EMEC", "Tester")
        self.min_deg_per_sec = self.settings.value("min_deg_per_sec", 1, type=int)
        self.tolerance = self.settings.value("L2L3_target_tolerance", 20, type=int)
        self.auto_start_test = self.settings.value("auto_start_test", True, type=bool)

        self.io.set_enable(False)

        self.timeout.connect(self.test_routine)  # connect test routine to timeout signal

        if self.auto_start_test:
            self.detect_presence_timer = QTimer()
            self.detect_presence_timer.timeout.connect(self.detect_presence)
            self.detect_presence_timer.start(1000)

    def __str__(self):
        return f"L2/L3 IO Drive"

    @property
    def serial_number(self) -> int:
        return self._serial_number

    @serial_number.setter
    def serial_number(self, sn: int) -> None:
        self._serial_number = sn

    @property
    def customer(self) -> str:
        return self._customer

    @customer.setter
    def customer(self, customer: str) -> None:
        self._customer = customer

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment: str) -> None:
        self._comment = comment

    def get_label(self):
        """
        Create a label and send a signal passing the label
        This method should be connected to a singnal (es. timeout signal)
        :return:
        """
        logger.debug(f"Create Label for serial number {self.serial_number}")
        label = Label(self.serial_number)
        label.type = str(self)
        label.node_id = IO_DRIVE_SLEWING_ID

        return label

    def detect_presence(self):
        if self.io.get_ai_voltage_range() == 1:  # voltage in range
            if self.drive_present_since < 1:
                self.drive_present_since += 1
            else:
                if not self.isActive() and self.drive_removed:
                    logger.debug(f"Drive connected on IO {self.io}")
                    self.drive_removed = False
                    self.label_ready = False
                    if self.settings.value("sn_mnt_active", True, type=bool):
                        dialog = AddSNDialog(node_id=IO_DRIVE_SLEWING_ID)
                        self.serial_number = dialog.serial_number
                    self.start_test()
        else:
            if self.drive_present_since > 0:
                self.drive_present_since = 0
                self.drive_removed = True

                logger.debug(f"Drive removed on IO {self.io}")

                if self. isActive():
                    self.stop_test(message="Drive removed")

                if self.label_ready:
                    self.on_print_label.emit(self.serial_number)

    def get_actual_angle(self) -> float:
        return self.io.get_actual_angle()

    def get_elapsed_time(self) -> int:
        return self.elapsed_time

    def get_cw_movements(self) -> int:
        return self.cw_movements

    def get_ccw_movements(self) -> int:
        return self.ccw_movements

    def reset_counters(self):
        self.cw_movements = 0
        self.ccw_movements = 0

    def get_status(self) -> str:
        if self.test_error_message is not None:
            return self.test_error_message

        if self.io.get_ai_voltage_range() == 1:
            return "OK"
        elif self.io.get_ai_voltage_range() == 0:
            return f"Not connected or angle voltage < {self.io.min_voltage_at_0_deg}V"
        elif self.io.get_ai_voltage_range() == 2:
            return f"Angle voltage > {self.io.max_voltage_at_360_deg}V"

    def start_movement(self):
        mid_target = self.io.min_angle + (self.io.max_angle - self.io.min_angle) / 2

        if self.io.get_actual_angle() > mid_target:
            self.moving_direction = CW
            self.io.set_direction(False)
            self.cw_movements += 1
            logger.debug(f"Start CW movement on IO {self.io}")
        else:
            self.moving_direction = CCW
            self.io.set_direction(True)
            self.ccw_movements += 1
            logger.debug(f"Start CCW movement on IO {self.io}")

        self.io.set_enable(True)

    def stop_movement(self):
        logger.debug(f"Stop movement on IO {self.io}")
        try:
            self.io.set_enable(False)
        except Exception as e:
            logger.error(f'Cannot stop movement: {e}')

    def move_in_direction(self, direction):
        if self.moving_direction is not direction:
            self.moving_time = 0
            if direction == CW:
                self.io.set_direction(False)
                self.moving_direction = CW
                self.cw_movements += 1
            else:
                self.io.set_direction(True)
                self.moving_direction = CCW
                self.ccw_movements += 1

    def start_test(self):
        if self.isActive():
            logger.debug(f"Test already running on this IO's")
            return

        self.moving_time = self.not_moving_counter = self.wrong_movement_counter = 0
        self.test_error_message = None

        # at every start take setting of label printer timer
        self.label_print_timeout = int(self.settings.value("label_print_timer", 60))

        self.start_movement()
        self.start(1000)
        # logger.debug(f"Start SlewingTester on IO {self.io}")

    def stop_test(self, message: str = None):
        if not self.isActive():
            return

        if message is not None:
            self.test_error_message = message
            logger.debug(f'Stop Test on IO {self.io} with message: {message}')
        else:
            logger.debug(f'Stop Test on IO {self.io}')

        self.stop_movement()
        self.stop()  # stop timer
        self.reset_counters()  # reset movement counters

        self.moving_time = self.elapsed_time = self.not_moving_counter = self.elapsed_time_2_temp = 0

    def test_routine(self):
        self.elapsed_time += 1

        actual_angle = self.io.get_actual_angle()

        min_limit = abs(self.io.min_angle) + self.tolerance
        max_limit = abs(self.io.max_angle) - self.tolerance

        if max_limit <= actual_angle:  # max position reached condition
            self.move_in_direction(CCW)
        elif actual_angle <= min_limit:  # min position reached condition
            self.move_in_direction(CW)
        else:
            self.moving_time += 1

        if min_limit < actual_angle < max_limit:  # between limits
            # detect max movement time exceeded
            if self.moving_time >= MAX_MOVEMENT_TIME_ABSOLUTE_SLEWING:
                self.stop_test(message=f"Max movement time of {MAX_MOVEMENT_TIME_ABSOLUTE_SLEWING}s exceeded!!")

            # check if drive is moving
            if abs(self.actual_angle_temp - actual_angle) < self.min_deg_per_sec:  # is not moving??
                self.not_moving_counter += 1
                if self.not_moving_counter >= 4:
                    self.stop_test(message=f"Slewing is not moving since {self.not_moving_counter}s")
            else:
                self.not_moving_counter = 0  # reset counter for detection "not moving" error

                if self.actual_angle_temp > actual_angle:  # is drive moving CCW?
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

                if self.wrong_movement_counter >= 10:
                    self.stop_test(message=f"Slewing is moving in wrong direction since {self.wrong_movement_counter}")

                # update temp every second cycle
                if self.elapsed_time - self.elapsed_time_2_temp >= 2:
                    self.elapsed_time_2_temp = self.elapsed_time  # update temp for elapsed time
                    self.actual_angle_temp = actual_angle  # update temp for actual position

        # generate signal for printing/generating a label
        if not self.label_ready and self.elapsed_time > self.label_print_timeout:
            self.label_ready = True
            label = self.get_label()
            self.on_label_ready.emit(label)

