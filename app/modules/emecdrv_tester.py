import time
import logging
from canopen import BaseNode402
from canopen.emcy import EmcyError
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QSettings, QTimer

from defines import *
from utils import CurrentStatistics, compare_versions

logger = logging.getLogger(__name__)


class EMECDrvTester(QTimer):
    on_test_timer_timeout = pyqtSignal()
    generate_label_signal = pyqtSignal()

    # statistics for current values used for min, max, mean, stdev on fifo values
    current_stat = CurrentStatistics(max_length=20)

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
        self.min_target = None
        self.max_target = None
        self.tolerance = None
        self.target_temp = None

        self.settings = QSettings("EMEC", "Tester")

        # register emergency error callback that will stop with error message from canopen
        self.node.emcy.add_callback(self.emergency_callback)

        # Node initialisation
        node.nmt.state = 'OPERATIONAL'
        node.sdo[OD_MODES_OF_OPERATION].raw = PROFILE_POSITION_OPERATING_MODE  # “Profile Position” operating mode

        self.init_node_state('READY TO SWITCH ON')
        self.init_node_state('SWITCHED ON')
        self.init_node_state('OPERATION ENABLED')

    def init_node_state(self, state):
        timeout = time.time() + 15
        self.node.state = state
        while self.node.state != state:
            if time.time() > timeout:
                raise Exception(f'Timeout when trying to change state to {state}')
            time.sleep(0.001)

    @property
    def max_error_current(self):
        """ Max current in mA for over-current detection """
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
        """ Minimum target value that drive will reach during test process """
        return self._min_target

    @min_target.setter
    def min_target(self, target: int):
        self._min_target = target

    @property
    def max_target(self):
        """ Maximum target value that drive will reach during test process """
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
        """ Return's manufacturer device name red from canopen registers """
        return self.node.sdo[OD_MANUFACTURER_DEVICE_NAME].raw

    @property
    def manufacturer_hardware_version(self):
        """ Return's manufacturer hardware version red from canopen registers """
        return self.node.sdo[OD_MANUFACTURER_HARDWARE_VERSION].raw

    @property
    def manufacturer_software_version(self):
        """ Return's manufacturer software version red from canopen registers """
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
        error_messages = {
            0x01: "Over current error",
            0x02: "Over temperature error",
            0x04: "Position controller error",
            0x08: "Following error"
        }

        try:
            flag = self.node.sdo[OD_DEVICE_ERROR_FLAGS].raw
        except Exception as e:
            flag = 0
            logger.debug(e)

        errors = [msg for bit, msg in error_messages.items() if flag & bit]
        return ", ".join(errors)

    def emergency_callback(self, error: EmcyError):
        error_messages = {
            0x0000: "Fault reset",
            0x2310: "Over current on motor driver",
            0x4310: "Over temperature error",
            0x8110: "CAN controller overflow",
            0x8120: "CAN error passive",
            0x8130: "Life guard error or heartbeat error",
            0x8140: "CAN controller recovered from bus-off state",
            0x8210: "PDO not processed due to length error",
            0x8220: "PDO length exceeded",
            0x8500: "Position controller",
            0x8611: "Following error"
        }

        if error.code in error_messages:
            self.stop_test(f"CANOpen error ({hex(error.code)}): {error_messages[error.code]}")

    def get_elapsed_time(self) -> int:
        return self.elapsed_time

    @property
    def status(self) -> str:
        if self.test_error_message:
            return self.test_error_message

        state = self.node.state
        if self.isActive() and state == 'OPERATION ENABLED':
            return "Test running"
        elif not self.isActive() and state == 'SWITCHED ON':
            return "Stopped"

        return state

    def goto_target_position(self, position: int):
        if self.actual_position > abs(position):  # abs() because slewing have negative value when turning CCW
            self.moving_direction = CCW
        elif self.actual_position < abs(position):
            self.moving_direction = CW
        else:
            self.moving_direction = STOPPED
            self.stop_test("Internal error: New target position same  as actual")

        self.stop_movement()
        self.node.sdo[OD_TARGET_POSITION].raw = self.target_temp = position  # set new target position
        QTimer.singleShot(1500, self.start_movement)  # wait 1,5s until restart movement in opposite direction
        self.moving_time = 0  # Reset timer when reaching target position

    def timeout_stat(self):
        try:
            self.current_stat.add(self.current_actual_value)  # add current value to statistics
        except Exception as e:
            logger.debug(f'Cannot read actual current from SDO: {e}')

    def timeout_test(self):
        """
        Functions in this method:
            -This method is called every second by QTimer to check conditions of test:
                - max movement time exceeded
                - mean current exceeds max current limit
                - drive is not moving
                - drive is moving in wrong direction

            -This method also generates signal for printing/generating a label
            -This method also stops test if error is detected
            -This method also manages target position change when min/max position is reached
        """

        self.elapsed_time = self.elapsed_time + 1
        self.on_test_timer_timeout.emit()

        # detect max movement time exceeded
        if self.moving_time >= MAX_MOVEMENT_TIME_ABSOLUTE:
            self.stop_test(f"Max movement time of {MAX_MOVEMENT_TIME_ABSOLUTE}s exceeded!!")

        try:
            # check max current limit
            mean = self.current_stat.mean()
            if mean > self.max_error_current:
                self.stop_test(f"Current limit exceeded (Imean= {mean} mA)")

            # check if drive is moving
            if self.actual_position_temp == self.actual_position:  # is not moving??
                self.not_moving_counter += 1
                # logger.debug(f"Actual position not changing since {self.not_moving_counter}s")
                if self.not_moving_counter >= 4:
                    self.stop_test(f"Drive is not moving since {self.not_moving_counter}s")

            else:
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
                self.moving_time += 1  # increment timer during movement

            # generate signal for printing/generating a label
            if not self.label_printed and self.elapsed_time > self.label_print_timeout:
                self.generate_label_signal.emit()
                self.label_printed = True

        except Exception as e:
            logger.debug(f'Exception during testing routine: {e}')
            self.stop()

    def stop_test(self, message: str = None):
        self.test_error_message = message if message else None
        logger.debug(f'Stop Test on Node {self.node.id} due to {message if message else ""}')

        try:
            self.stop_movement()
        except Exception as e:
            logger.debug(f"Error sending stop command to device: {e}")

        self.moving_time = self.elapsed_time = self.not_moving_counter = 0
        self.current_stat.reset()
        self.stop()

    def start_movement(self):
        try:
            control_word = self.node.sdo[OD_CONTROL_WORD].raw
            control_word |= CONTROL_ENABLE_OPERATION
            control_word &= ~CONTROL_START_MOVEMENT_ORDER
            control_word |= CONTROL_START_MOVEMENT_ORDER
            self.node.sdo[OD_CONTROL_WORD].raw = control_word

            self.timeout.connect(self.timeout_stat)
        except Exception as e:
            logger.debug(f'Cannot start movement: {e}')

    def stop_movement(self):
        try:
            self.node.sdo[OD_CONTROL_WORD].raw &= ~CONTROL_ENABLE_OPERATION
        except Exception as e:
            logger.debug(f'Cannot stop movement: {e}')
        finally:
            self.timeout.disconnect(self.timeout_stat)

    def ack_error(self):
        try:
            control_word = self.node.sdo[OD_CONTROL_WORD].raw
            self.node.sdo[OD_CONTROL_WORD].raw = control_word ^ CONTROL_ACK_ERROR
            self.node.sdo[OD_CONTROL_WORD].raw = control_word
        except Exception as e:
            logger.debug(f"Error during ack_error: {e}")
        self.test_error_message = None


class SlewingTester(EMECDrvTester):
    def __init__(self, node: BaseNode402):
        super().__init__(node)

        self.min_target = MIN_TARGET_POSITION_SLEWING
        self.max_target = MAX_TARGET_POSITION_SLEWING
        self.target_temp = (self.max_target - self.min_target) / 2 + self.min_target  # get mid-position
        self.tolerance = 10
        self.max_error_current = int(self.settings.value("max_error_current_slewing", 600))

        logger.debug(f"SlewingTester created with node_id: {node.id}")

        self.timeout.connect(self.timeout_test)

    def get_software_version_ok(self) -> bool:
        version = self.settings.value("min_sw_version_slewing", "v1.25")
        return compare_versions(self.manufacturer_software_version, version) >= 0

    def start_test(self):
        if not self.isActive():
            try:
                self.moving_time = 0
                self.not_moving_counter = 0  # counter for detection of no movement error
                self.wrong_movement_counter = 0  # counter for detection of wrong movement error
                self.test_error_message = None

                self.max_error_current = int(self.settings.value("max_error_current_slewing", 600))
                self.label_print_timeout = int(self.settings.value("label_print_timer", 60))

                # Init target first time min or max depending on actual position
                mid = (self.max_target - self.min_target) / 2 + self.min_target  # get mid-position

                if self.node.sdo[OD_TARGET_POSITION].raw > mid:
                    # move in CW direction
                    self.node.sdo[OD_TARGET_POSITION].raw = self.max_target
                    self.moving_direction = CW
                else:
                    # move in CCW direction
                    self.node.sdo[OD_TARGET_POSITION].raw = self.min_target
                    self.moving_direction = CCW

                self.start_movement()
                self.start(1000)
                logger.debug(f"Start SlewingTester for Node: {self.node.id} on network {self.node.network}")

            except Exception as e:
                logger.debug(f"Error starting test: {e}")


class LiftTester(EMECDrvTester):
    def __init__(self, node: BaseNode402):
        super().__init__(node)

        self.min_target = MIN_TARGET_POSITION_LIFT
        self.max_target = MAX_TARGET_POSITION_LIFT
        self.target_temp = (self.max_target - self.min_target) / 2 + self.min_target  # get mid-position
        self.tolerance = 0
        self.max_error_current = int(self.settings.value("max_error_current_lift", 800))

        logger.debug(f"LiftTester created with node_id: {node.id}")

        self.timeout.connect(self.timeout_test)

    def get_software_version_ok(self) -> bool:
        version = self.settings.value("min_sw_version_lift", "v3.16")
        return compare_versions(self.manufacturer_software_version, version) >= 0

    def start_test(self):
        if not self.isActive():
            try:
                self.moving_time = 0
                self.not_moving_counter = 0  # counter for detection of no movement error
                self.wrong_movement_counter = 0  # counter for detection of wrong movement error
                self.test_error_message = None

                self.max_error_current = int(self.settings.value("max_error_current_lift", 800))
                self.label_print_timeout = int(self.settings.value("label_print_timer", 60))

                # Init target first time min or max depending on actual position
                mid = (self.max_target - self.min_target) / 2 + self.min_target  # get mid-position

                if self.node.sdo[OD_TARGET_POSITION].raw > mid:
                    # move in CW direction
                    self.node.sdo[OD_TARGET_POSITION].raw = self.max_target
                    self.moving_direction = CW
                else:
                    # move in CCW direction
                    self.node.sdo[OD_TARGET_POSITION].raw = self.min_target
                    self.moving_direction = CCW

                self.start_movement()
                self.start(1000)
                logger.debug(f"Start LiftTester for Node: {self.node.id} on network {self.node.network}")

            except Exception as e:
                logger.debug(f"Error starting test: {e}")

