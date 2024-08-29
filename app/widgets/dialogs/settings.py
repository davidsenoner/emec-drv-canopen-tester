import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog

from app.widgets.ui_settings_diag import Ui_SettingsDialog

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """
    Settings Dialog
    """
    def __init__(self):
        super().__init__()

        # load UI
        self._ui = Ui_SettingsDialog()
        self._ui.setupUi(self)

        self.settings = QSettings("EMEC", "Tester")  # init QSettings

        # test procedure settings
        self._ui.sb_norm_run_slewing_duration.setValue(self.settings.value("norm_run_slewing_duration", 200, type=int))
        self._ui.cb_repeat_test.setChecked(self.settings.value("repeat_test_active", True, type=bool))
        self._ui.sb_min_torque.setValue(self.settings.value("min_torque", 38, type=int))
        self._ui.sb_max_torque.setValue(self.settings.value("max_torque", 52, type=int))

        # interface settings
        self._ui.cb_enable_can0.setChecked(self.settings.value("can0_enabled", True, type=bool))
        self._ui.cb_enable_can1.setChecked(self.settings.value("can1_enabled", True, type=bool))
        self._ui.cb_enable_can2.setChecked(self.settings.value("can2_enabled", False, type=bool))
        self._ui.cb_enable_can3.setChecked(self.settings.value("can3_enabled", False, type=bool))
        self._ui.cb_enable_can4.setChecked(self.settings.value("can4_enabled", False, type=bool))

        self._ui.ldt_baudrate_can0.setText(self.settings.value("can0_baudrate", 125000, type=str))
        self._ui.ldt_baudrate_can1.setText(self.settings.value("can1_baudrate", 125000, type=str))
        self._ui.ldt_baudrate_can2.setText(self.settings.value("can2_baudrate", 125000, type=str))
        self._ui.ldt_baudrate_can3.setText(self.settings.value("can3_baudrate", 125000, type=str))
        self._ui.ldt_baudrate_can4.setText(self.settings.value("can4_baudrate", 125000, type=str))

        self._ui.ldt_remote_io_ip.setText(self.settings.value("remote_io_ip", "192.168.23.254", type=str))
        self._ui.ldt_remote_io_port.setText(self.settings.value("remote_io_port", 502, type=str))
        self._ui.sb_remote_io_connection_timeout.setValue(self.settings.value("remote_io_connection_timeout", 5, type=int))
        self._ui.sb_remote_io_rw_period.setValue(self.settings.value("remote_io_rw_period", 0.5, type=float))

        # IO Drives settings
        self._ui.cb_remote_io_enable.setChecked(self.settings.value("remote_io_enabled", True, type=bool))
        self._ui.cb_EN0_active_high.setChecked(self.settings.value("EN0_active_high", True, type=bool))
        self._ui.cb_EN1_active_high.setChecked(self.settings.value("EN1_active_high", True, type=bool))
        self._ui.cb_DIR0_active_high.setChecked(self.settings.value("DIR0_active_high", True, type=bool))
        self._ui.cb_DIR1_active_high.setChecked(self.settings.value("DIR1_active_high", True, type=bool))

        self._ui.sb_AI0_voltage_0deg.setValue(self.settings.value("AI0_voltage_0deg", 0.5, type=float))
        self._ui.sb_AI0_voltage_359deg.setValue(self.settings.value("AI0_voltage_359deg", 4.5, type=float))
        self._ui.sb_AI1_voltage_0deg.setValue(self.settings.value("AI1_voltage_0deg", 0.5, type=float))
        self._ui.sb_AI1_voltage_359deg.setValue(self.settings.value("AI1_voltage_359deg", 4.5, type=float))

        self._ui.sp_io_drive_0_enable_pin.setValue(self.settings.value("io_drive_0_enable_pin", 0, type=int))
        self._ui.sp_io_drive_0_direction_pin.setValue(self.settings.value("io_drive_0_direction_pin", 1, type=int))
        self._ui.sp_io_drive_0_angle_pin.setValue(self.settings.value("io_drive_0_angle_pin", 0, type=int))
        self._ui.sp_io_drive_1_enable_pin.setValue(self.settings.value("io_drive_1_enable_pin", 2, type=int))
        self._ui.sp_io_drive_1_direction_pin.setValue(self.settings.value("io_drive_1_direction_pin", 3, type=int))
        self._ui.sp_io_drive_1_angle_pin.setValue(self.settings.value("io_drive_1_angle_pin", 1, type=int))

        # L2/L3 drives test settings
        self._ui.sp_l2l3_target_pos_tolerance.setValue(self.settings.value("L2L3_target_tolerance", 20, type=int))

        ret = self.exec_()

        # if exit with OK
        if ret == QDialog.Accepted:
            # test procedure settings
            self.settings.setValue("norm_run_slewing_duration", self._ui.sb_norm_run_slewing_duration.value())
            self.settings.setValue("repeat_test_active", self._ui.cb_repeat_test.isChecked())
            self.settings.setValue("min_torque", self._ui.sb_min_torque.value())
            self.settings.setValue("max_torque", self._ui.sb_max_torque.value())

            # interface settings
            self.settings.setValue("can0_enabled", self._ui.cb_enable_can0.isChecked())
            self.settings.setValue("can1_enabled", self._ui.cb_enable_can1.isChecked())
            self.settings.setValue("can2_enabled", self._ui.cb_enable_can2.isChecked())
            self.settings.setValue("can3_enabled", self._ui.cb_enable_can3.isChecked())
            self.settings.setValue("can4_enabled", self._ui.cb_enable_can4.isChecked())

            try:
                self.settings.setValue("can0_baudrate", int(self._ui.ldt_baudrate_can0.text()))
            except ValueError:
                logger.error("Invalid value for CAN0 baudrate")

            try:
                self.settings.setValue("can1_baudrate", int(self._ui.ldt_baudrate_can1.text()))
            except ValueError:
                logger.error("Invalid value for CAN1 baudrate")

            try:
                self.settings.setValue("can2_baudrate", int(self._ui.ldt_baudrate_can2.text()))
            except ValueError:
                logger.error("Invalid value for CAN2 baudrate")

            try:
                self.settings.setValue("can3_baudrate", int(self._ui.ldt_baudrate_can3.text()))
            except ValueError:
                logger.error("Invalid value for CAN3 baudrate")

            try:
                self.settings.setValue("can4_baudrate", int(self._ui.ldt_baudrate_can4.text()))
            except ValueError:
                logger.error("Invalid value for CAN4 baudrate")

            self.settings.setValue("remote_io_ip", self._ui.ldt_remote_io_ip.text())

            try:
                self.settings.setValue("remote_io_port", int(self._ui.ldt_remote_io_port.text()))
            except ValueError:
                logger.error("Invalid value for Remote IO port")

            self.settings.setValue("remote_io_connection_timeout", self._ui.sb_remote_io_connection_timeout.value())
            self.settings.setValue("remote_io_rw_period", self._ui.sb_remote_io_rw_period.value())

            # IO Drives settings
            self.settings.setValue("remote_io_enabled", self._ui.cb_remote_io_enable.isChecked())
            self.settings.setValue("EN0_active_high", self._ui.cb_EN0_active_high.isChecked())
            self.settings.setValue("EN1_active_high", self._ui.cb_EN1_active_high.isChecked())
            self.settings.setValue("DIR0_active_high", self._ui.cb_DIR0_active_high.isChecked())
            self.settings.setValue("DIR1_active_high", self._ui.cb_DIR1_active_high.isChecked())

            self.settings.setValue("AI0_voltage_0deg", self._ui.sb_AI0_voltage_0deg.value())
            self.settings.setValue("AI0_voltage_359deg", self._ui.sb_AI0_voltage_359deg.value())
            self.settings.setValue("AI1_voltage_0deg", self._ui.sb_AI1_voltage_0deg.value())
            self.settings.setValue("AI1_voltage_359deg", self._ui.sb_AI1_voltage_359deg.value())

            self.settings.setValue("io_drive_0_enable_pin", self._ui.sp_io_drive_0_enable_pin.value())
            self.settings.setValue("io_drive_0_direction_pin", self._ui.sp_io_drive_0_direction_pin.value())
            self.settings.setValue("io_drive_0_angle_pin", self._ui.sp_io_drive_0_angle_pin.value())
            self.settings.setValue("io_drive_1_enable_pin", self._ui.sp_io_drive_1_enable_pin.value())
            self.settings.setValue("io_drive_1_direction_pin", self._ui.sp_io_drive_1_direction_pin.value())
            self.settings.setValue("io_drive_1_angle_pin", self._ui.sp_io_drive_1_angle_pin.value())

            # L2/L3 drives test settings
            self.settings.setValue("L2L3_target_tolerance", self._ui.sp_l2l3_target_pos_tolerance.value())



