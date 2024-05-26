import time
import logging
from canopen import BaseNode402
from canopen.emcy import EmcyError
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QSettings, QTimer

from app.modules.defines import *
from app.modules.utils import CurrentStatistics, compare_versions

logger = logging.getLogger(__name__)

NORMAL_RUN_TEST_MODE = 0
CW_BLOCKED_TEST_MODE = 1
CCW_BLOCKED_TEST_MODE = 2


class EMECDrvTester(QTimer):
    on_test_timer_timeout = pyqtSignal()
    generate_label_signal = pyqtSignal()

    def __init__(self, node: BaseNode402):
        super().__init__()

        self.node = node
        self.label_print_timeout = None
        self.not_moving_counter = 0  # counter for detection of no movement error
        self.wrong_movement_counter = 0  # counter for detection of wrong movement error
        self.actual_position_temp = 0
        self.label_printed = False  # status bit True=Label already printed

        self.settings = QSettings("EMEC", "Tester")

        self.moving_time = 0
        self.elapsed_time = 0
        self.test_error_message = ""  # Message to show to screen
        self.moving_direction = CW  # CCW, CW, STOPPED

        if node.id == TITAN40_EMECDRV5_LIFT_NODE_ID:
            self.min_target = MIN_TARGET_POSITION_LIFT,  # default for Lift
            self.max_target = MAX_TARGET_POSITION_LIFT  # default for Lift
            self.max_error_current = int(self.settings.value("max_error_current_lift", 600))
            self.tolerance = 0

        elif node.id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            self.min_target = MIN_TARGET_POSITION_SLEWING
            self.max_target = MAX_TARGET_POSITION_SLEWING
            self.max_error_current = int(self.settings.value("max_error_current_slewing", 600))
            self.tolerance = 10

        self.target_temp = (self.max_target - self.min_target) / 2 + self.min_target  # get mid-position

        self.statistic_timer = QTimer()
        self.statistic_timer.setInterval(1000)
        self.statistic_timer.timeout.connect(self.timer_statistics)

        # statistics for current values used for min, max, mean, stdev on fifo values
        self.current_stat = CurrentStatistics(max_length=20)
        self.block_current_stat = CurrentStatistics(max_length=5)

        # register emergency error callback that will stop with error message from canopen
        self.node.emcy.add_callback(self.emergency_callback)

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

        self.timeout.connect(self.test_routine)  # connect test routine to timeout signal

    def get_ccw_movements(self):
        """ Return's CCW movements red from canopen registers """
        return self.node.sdo[0x2000][1].raw

    def get_accumulative_operating_time(self):
        """ Return's accumulative operating time red from canopen registers """
        return self.node.sdo[0x2000][0].raw

    def get_device_temp(self):
        """ Return's device temperature red from canopen registers """
        return self.node.sdo[0x2001][0].raw

    def get_max_device_temp(self):
        """ Return's max device temperature red from canopen registers """
        return self.node.sdo[0x2001][1].raw

    def get_cw_movements(self):
        """ Return's CW movements red from canopen registers """
        return self.node.sdo[0x2000][2].raw

    def get_actual_position(self):
        """ Return's actual position red from canopen registers """
        return self.node.sdo[OD_POSITION_ACTUAL_VALUE].raw

    def get_target_position(self):
        """ Return's target position red from canopen registers """
        return self.node.sdo[OD_TARGET_POSITION].raw

    def get_max_current(self):
        return self.node.sdo[OD_MAX_CURRENT].raw

    def get_rated_current(self):
        """ Return's rated current red from canopen registers """
        return self.node.sdo[OD_MOTOR_RATED_CURRENT].raw

    def get_actual_current(self):
        rated_current = self.node.sdo[OD_MOTOR_RATED_CURRENT].raw
        actual_current = self.node.sdo[OD_CURRENT_ACTUAL_VALUE].raw * (rated_current / 1000)
        return actual_current

    def get_dc_link_circuit_voltage(self):
        """ Return's DC link circuit voltage red from canopen registers """
        return self.node.sdo[OD_DC_LINK_CIRCUIT_VOLTAGE].raw

    def get_control_word(self):
        """ Return's control word red from canopen registers """
        return self.node.sdo[OD_CONTROL_WORD].raw

    def get_status_word(self):
        """ Return's status word red from canopen registers """
        return self.node.sdo[OD_STATUS_WORD].raw

    def get_manufacturer_device_name(self):
        """ Return's manufacturer device name red from canopen registers """
        return self.node.sdo[OD_MANUFACTURER_DEVICE_NAME].raw

    def get_manufacturer_hardware_version(self):
        """ Return's manufacturer hardware version red from canopen registers """
        return self.node.sdo[OD_MANUFACTURER_HARDWARE_VERSION].raw

    def get_manufacturer_software_version(self):
        """ Return's manufacturer software version red from canopen registers """
        return self.node.sdo[OD_MANUFACTURER_SOFTWARE_VERSION].raw

    def get_software_version_ok(self) -> bool:
        # compare software version
        min_sw_version = 0

        # load min software version from settings depending on drive type
        if self.node.id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            min_sw_version = self.settings.value("min_sw_version_slewing", "v1.25")
        elif self.node.id == TITAN40_EMECDRV5_LIFT_NODE_ID:
            min_sw_version = self.settings.value("min_sw_version_lift", "v3.16")

        # compare min sw version with version from drive
        software_comparison = compare_versions(self.get_manufacturer_software_version(), min_sw_version)

        return software_comparison >= 0

    def get_elapsed_time(self) -> int:
        return self.elapsed_time

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
            logger.error(e)

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
            self.stop_test(message=f"CANOpen error ({hex(error.code)}): {error_messages[error.code]}")

    def get_status(self) -> str:
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
        try:
            actual_position = self.get_actual_position()
            if actual_position > abs(position):  # abs() because slewing have negative value when turning CCW
                self.moving_direction = CCW
            elif actual_position < abs(position):
                self.moving_direction = CW
            else:
                self.moving_direction = STOPPED
                self.stop_test(message="Internal error: New target position same  as actual")

            self.stop_movement()

            self.node.sdo[OD_TARGET_POSITION].raw = self.target_temp = position  # set new target position
            QTimer.singleShot(1500, self.start_movement)  # wait 1,5s until restart movement in opposite direction
            self.moving_time = 0  # Reset timer when reaching target position
        except Exception as e:
            logger.error(f'Cannot go to target position: {e}')

    def timer_statistics(self):
        try:
            actual_current = self.get_actual_current()
            self.current_stat.add(actual_current)  # add current value to statistics
            self.block_current_stat.add(actual_current)  # add current value to statistics
        except Exception as e:
            logger.error(f'Cannot read actual current from SDO: {e}')

    def stop_test(self, message: str = None):
        if message is not None:
            self.test_error_message = message
            logger.debug(f'Stop Test on Node {self.node.id} due to {message}')
        else:
            logger.debug(f'Stop Test on Node {self.node.id}')

        self.stop_movement()
        self.stop()  # stop timer

        self.moving_time = self.elapsed_time = self.not_moving_counter = 0
        self.current_stat.reset()  # reset current statistics
        self.block_current_stat.reset()  # reset current statistics

    def start_movement(self):
        try:
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw | CONTROL_ENABLE_OPERATION

            # A rising flank starts a movement order
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_START_MOVEMENT_ORDER
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw | CONTROL_START_MOVEMENT_ORDER

            self.timeout.connect(self.timer_statistics)  # connect statistics timer to timeout signal
        except Exception as e:
            logger.error(f'Cannot start movement: {e}')

    def stop_movement(self):
        try:
            self.node.sdo[OD_CONTROL_WORD].raw = self.node.sdo[OD_CONTROL_WORD].raw & ~CONTROL_ENABLE_OPERATION
        except Exception as e:
            logger.error(f'Cannot stop movement: {e}')

        self.timeout.disconnect(self.timer_statistics)  # disconnect statistics timer from timeout signal

    def ack_error(self):
        try:
            control_word = self.node.sdo[OD_CONTROL_WORD].raw
            self.node.sdo[OD_CONTROL_WORD].raw = control_word ^ CONTROL_ACK_ERROR
            self.node.sdo[OD_CONTROL_WORD].raw = control_word
        except Exception as e:
            logger.error(f"Error during ack_error: {e}")
        self.test_error_message = None


class SlewingTester(EMECDrvTester):
    def __init__(self, node: BaseNode402):
        super().__init__(node)

        logger.debug(f"SlewingTester created with node_id: {node.id}, instance {self}")

        self.tolerance = 10
        self.actual_test_mode = 0
        self.cw_block_detected = False
        self.ccw_block_detected = False
        self.label_print_timeout = None
        self.actual_position_temp = 0
        self.label_printed = False  # status bit True=Label already printed
        self._actual_test_mode_description = "Normal running"
        self.wrong_movement_counter = 0  # counter for detection of wrong movement error
        self.min_target = MIN_TARGET_POSITION_SLEWING
        self.max_target = MAX_TARGET_POSITION_SLEWING
        self.target_temp = (self.max_target - self.min_target) / 2 + self.min_target  # get mid-position

        # load settings from QSettings
        self.max_error_current = int(self.settings.value("max_error_current_slewing", 600))
        self.normal_run_test_duration = int(self.settings.value("norm_run_slewing_duration", 120))
        self.min_tld_block_duration = int(self.settings.value("min_tld_block_duration", 4))
        self.block_current_threshold = int(self.settings.value("block_current_threshold", 1500))

        self.timeout.connect(self.test_routine)  # connect test routine to timeout signal

    def get_software_version_ok(self) -> bool:
        version = self.settings.value("min_sw_version_slewing", "v1.25")
        return compare_versions(self.get_manufacturer_software_version(), version) >= 0

    def get_test_mode_description(self) -> str:
        return self._actual_test_mode_description

    def is_max_limit_reached(self):
        """ Return True if max limit is reached """
        try:
            actual_position = self.get_actual_position()
            return (abs(self.max_target) - self.tolerance) <= actual_position
        except Exception as e:
            self.stop()
            logger.error(f'Cannot read actual position from SDO: {e}')
            return False

    def is_min_limit_reached(self):
        """ Return True if min limit is reached """
        try:
            actual_position = self.get_actual_position()
            return actual_position <= (abs(self.min_target) + self.tolerance)
        except Exception as e:
            logger.error(f'Cannot read actual position from SDO: {e}')
            return False

    def start_test(self):
        if not self.isActive():
            try:
                self.moving_time = 0
                self.not_moving_counter = 0  # counter for detection of no movement error
                self.wrong_movement_counter = 0  # counter for detection of wrong movement error
                self.test_error_message = None

                self.max_error_current = int(self.settings.value("max_error_current_slewing", 600))
                self.label_print_timeout = int(self.settings.value("label_print_timer", 60))
                self.normal_run_test_duration = int(self.settings.value("norm_run_slewing_duration", 120))
                self.min_tld_block_duration = int(self.settings.value("min_tld_block_duration", 5))
                self.block_current_threshold = int(self.settings.value("block_current_threshold", 1500))

                self.block_current_stat.set_threshold(self.block_current_threshold)

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

                self.actual_test_mode = NORMAL_RUN_TEST_MODE  # restart from normal, (0=normal running, 1=CW blocked, 2=CCW blocked)
                self._actual_test_mode_description = "Normal running"

                self.start_movement()
                self.start(1000)
                logger.debug(f"Start SlewingTester for Node: {self.node.id} on network {self.node.network}")

            except Exception as e:
                logger.error(f"Error starting test: {e}")

    def normal_running_test_routine(self):
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

        try:
            actual_position = self.get_actual_position()
        except Exception as e:
            self.stop()
            logger.error(f'Cannot read actual position from SDO: {e}')
            return

        # check max current limit
        mean = self.current_stat.mean()
        if mean > self.max_error_current:
            self.stop_test(message=f"Current limit exceeded (Imean= {mean} mA)")

        # check if drive is moving
        if 3 > abs(self.actual_position_temp - actual_position):  # is not moving??
            self.not_moving_counter += 1
            # logger.debug(f"Actual position not changing since {self.not_moving_counter}s")
            if self.not_moving_counter >= 4:
                self.stop_test(message=f"Slewing is not moving since {self.not_moving_counter}s")

        else:
            self.not_moving_counter = 0  # reset counter for detection "not moving" error
            if self.actual_position_temp > actual_position:  # is drive moving CCW?
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
                self.stop_test(message="Slewing is moving in wrong direction since {self.wrong_movement_counter}")

            self.actual_position_temp = actual_position  # update temp for actual position

        # after 2 minutes switch to CW blocked test mode
        if (self.elapsed_time > self.normal_run_test_duration) and self.is_min_limit_reached():

            # init CW blocked test mode
            self.cw_block_detected = False
            self._actual_test_mode_description = "CW blocked Test"
            self.block_current_stat.reset()  # start test with empty fifo
            self.actual_test_mode = CW_BLOCKED_TEST_MODE  # switch to CW blocked test mode

    def cw_block_test_routine(self):
        if self.block_current_stat.mean() >= self.block_current_threshold:
            self.cw_block_detected = True
            self._actual_test_mode_description = "CW blocked Test OK!!"
            logger.info("Block recognized in CW direction")

        if self.is_max_limit_reached():
            # a block event should be detected before reaching the max limit
            if not self.cw_block_detected:
                self.stop_test(message="Block not recognized in CW direction")  # stop test if block not recognized

            # init CCW blocked test mode
            self.ccw_block_detected = False
            self._actual_test_mode_description = "CCW blocked Test"
            self.block_current_stat.reset()  # start test with empty fifo
            self.actual_test_mode = CCW_BLOCKED_TEST_MODE  # switch to CCW blocked test mode

    def ccw_block_test_routine(self):

        if self.block_current_stat.mean() >= self.block_current_threshold:
            self.ccw_block_detected = True
            self._actual_test_mode_description = "CCW blocked Test OK!!"
            logger.info("Block recognized in CCW direction")

        if self.is_min_limit_reached():
            # a block event should be detected before reaching the min limit
            if not self.ccw_block_detected:
                self.stop_test(message="Block not recognized in CCW direction")  # stop test if block not recognized

            self.stop_test(message="Test finished successfully!!")

    def test_routine(self):
        """
        Test routine for slewing tester that will be called in timer and calls specific test mode routines
        """
        self.elapsed_time += 1
        self.on_test_timer_timeout.emit()

        try:
            actual_position = self.get_actual_position()
        except Exception as e:
            self.stop()
            logger.error(f'Cannot read actual position from SDO: {e}')
            return

        # detect max movement time exceeded
        if self.moving_time >= MAX_MOVEMENT_TIME_ABSOLUTE_SLEWING:
            self.stop_test(message=f"Max movement time of {MAX_MOVEMENT_TIME_ABSOLUTE_SLEWING}s exceeded!!")

        # max position reached condition
        if self.is_max_limit_reached():
            if self.target_temp != self.min_target:
                self.goto_target_position(self.min_target)  # go to the new position/other limit

        # min position reached condition
        elif self.is_min_limit_reached():
            if self.target_temp != self.max_target:
                self.goto_target_position(self.max_target)  # go to the new position/other limit

        # drive is moving condition
        else:
            self.moving_time += 1  # increment timer during movement

        # call test mode routines depending on actual test mode id
        if self.actual_test_mode == NORMAL_RUN_TEST_MODE:
            self.normal_running_test_routine()
        elif self.actual_test_mode == CW_BLOCKED_TEST_MODE:
            self.cw_block_test_routine()
        elif self.actual_test_mode == CCW_BLOCKED_TEST_MODE:
            self.ccw_block_test_routine()
        else:
            self._actual_test_mode_description = "Test mode unknown"
            logger.debug("Test mode unknown in test_routine()")
            self.stop_test(message="Stop test due to test mode unknown")

        # generate signal for printing/generating a label
        if not self.label_printed and self.elapsed_time > self.label_print_timeout:
            self.generate_label_signal.emit()
            self.label_printed = True


class LiftTester(EMECDrvTester):
    def __init__(self, node: BaseNode402):
        super().__init__(node)

        self.tolerance = 0
        self.label_print_timeout = None
        self.actual_test_mode_description = "Normal running"
        self.wrong_movement_counter = 0  # counter for detection of wrong movement error
        self.min_target = MIN_TARGET_POSITION_LIFT
        self.max_target = MAX_TARGET_POSITION_LIFT
        self.actual_position_temp = 0
        self.label_printed = False  # status bit True=Label already printed
        self.target_temp = (self.max_target - self.min_target) / 2 + self.min_target  # get mid-position
        self.max_error_current = int(self.settings.value("max_error_current_lift", 800))

        self.timeout.connect(self.test_routine)  # connect test routine to timeout signal

    def get_software_version_ok(self) -> bool:
        version = self.settings.value("min_sw_version_lift", "v3.16")
        return compare_versions(self.get_manufacturer_software_version(), version) >= 0

    def get_test_mode_description(self) -> str:
        return self.actual_test_mode_description

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

                self.actual_test_mode_description = "Normal running"

                self.start_movement()
                self.start(1000)
                logger.debug(f"Start LiftTester for Node: {self.node.id} on network {self.node.network}")

            except Exception as e:
                logger.error(f"Error starting test: {e}")

    def test_routine(self):
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

        self.elapsed_time += 1
        self.on_test_timer_timeout.emit()

        try:
            actual_position = self.get_actual_position()
        except Exception as e:
            self.stop()
            logger.error(f'Cannot read actual position from SDO: {e}')
            return

        # detect max movement time exceeded
        if self.moving_time >= MAX_MOVEMENT_TIME_ABSOLUTE_LIFT:
            self.stop_test(message=f"Max movement time of {MAX_MOVEMENT_TIME_ABSOLUTE_LIFT}s exceeded!!")

        # check max current limit
        mean = self.current_stat.mean()
        if mean > self.max_error_current:
            self.stop_test(message=f"Current limit exceeded (Imean= {mean} mA)")

        # check if drive is moving
        if 3 > abs(self.actual_position_temp - actual_position):  # is not moving??
            self.not_moving_counter += 1
            # logger.debug(f"Actual position not changing since {self.not_moving_counter}s")
            if self.not_moving_counter >= 4:
                self.stop_test(message=f"Lift is not moving since {self.not_moving_counter}s")

        else:
            self.not_moving_counter = 0  # reset counter for detection "not moving" error
            if self.actual_position_temp > actual_position:  # is drive moving CCW?
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
                self.stop_test(message=f"Lift is moving in wrong direction since {self.wrong_movement_counter}")

            self.actual_position_temp = actual_position  # update temp for actual position

        # max position reached condition
        if (abs(self.max_target) - self.tolerance) <= actual_position:
            if self.target_temp != self.min_target:
                self.goto_target_position(self.min_target)  # go to the new position

        # min position reached condition
        elif actual_position <= (abs(self.min_target) + self.tolerance):
            if self.target_temp != self.max_target:
                self.goto_target_position(self.max_target)  # go to the new position

        # drive is moving condition
        else:
            self.moving_time += 1  # increment timer during movement

        # generate signal for printing/generating a label
        if not self.label_printed and self.elapsed_time > self.label_print_timeout:
            self.generate_label_signal.emit()
            self.label_printed = True
