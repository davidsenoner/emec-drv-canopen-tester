import asyncio
import logging
import sys
import time

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer

from app.widgets.ui_main import Ui_MainWindow

from app.widgets.canopen_drives_table import CANOpenDrivesTable
from app.widgets.io_drives_table import IODrivesTable
from app.modules.io import CANOpenManger
from app.modules.io import MoxaE1242
from app.widgets.dialogs.settings import SettingsDialog
from app.widgets.dialogs.label_printer import LabelPrinterDialog
from app.modules.test_report import Label, TestReportManager

from PyQt5.QtCore import QSettings

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)-11s - %(levelname)-7s - %(message)s",
)

# Init canopen logger
logging.getLogger('can').setLevel(logging.ERROR)
logging.getLogger('canopen').setLevel(logging.ERROR)
logging.getLogger('canopen.sdo.client').setLevel(logging.CRITICAL)


class MainWindow(QMainWindow):
    def __init__(self, version: str):
        QMainWindow.__init__(self)

        logger.info(f"Starting EMEC Drive End-Of-Line Tester {version}")

        # Init UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.showMaximized()
        self.setWindowTitle(f"EMEC Drive End-Of-Line Tester {version}")  # Window title bar
        self.node_table = None
        self.moxa_remote_io = None
        self.canopen_manager = None

        # Settings management
        self.settings = QSettings("EMEC", "Tester")

        self._report_manager = TestReportManager()

        # CANOpen initialization
        channels = {
            0: {
                "enabled": self.settings.value("can0_enabled", True, type=bool),
                "baud": self.settings.value("can0_baudrate", 125000, type=str)
            },
            1: {
                "enabled": self.settings.value("can1_enabled", True, type=bool),
                "baud": self.settings.value("can1_baudrate", 125000, type=str)
            },
            2: {
                "enabled": self.settings.value("can2_enabled", False, type=bool),
                "baud": self.settings.value("can2_baudrate", 125000, type=str)
            },
            3: {
                "enabled": self.settings.value("can3_enabled", False, type=bool),
                "baud": self.settings.value("can3_baudrate", 125000, type=str)
            },
            4: {
                "enabled": self.settings.value("can4_enabled", False, type=bool),
                "baud": self.settings.value("can4_baudrate", 125000, type=str)
            }
        }
        self.canopen_manager = CANOpenManger(channels)

        # create drives tables
        if len(self.canopen_manager) > 0:  # at least ne channel detected
            self.node_table = CANOpenDrivesTable(self._ui.tbl_node_list, self.canopen_manager.items())  # Init Tables
            self.node_table.set_report_manager(self._report_manager)

        self._ui.lbl_detected_can_converter.setText(f"{len(self.canopen_manager)}")
        bauds = {cfg["baud"] for id, cfg in channels.items() if cfg.get("init", False)}
        self._ui.lbl_can_baudrate.setText(", ".join(map(str, bauds)))

        # Moxa remote IO initialization
        remote_io_enabled = self.settings.value("remote_io_enabled", True, type=bool)
        if remote_io_enabled:
            remote_io_ip = self.settings.value("remote_io_ip", "192.168.23.254", type=str)
            remote_io_port = self.settings.value("remote_io_port", 502, type=int)
            remote_io_connection_timeout = self.settings.value("remote_io_connection_timeout", 5, type=int)
            remote_io_rw_period = self.settings.value("remote_io_rw_period", 0.5, type=float)

            self.moxa_remote_io = MoxaE1242(ip=remote_io_ip, port=remote_io_port, rw_period=remote_io_rw_period)
            for _ in range(remote_io_connection_timeout):
                if self.moxa_remote_io.status:
                    break
                time.sleep(1)

            if self.moxa_remote_io.status:
                logger.info("Moxa E1242 Remote IO initialized")
                logger.info(f"CANOpen Manager initialized with {len(self.canopen_manager)} channels")
                logger.info(f"Moxa IP: {self.moxa_remote_io.lan_ip} - {self.moxa_remote_io.lan_mac}")

                self._ui.lbl_remoteio_ip.setText(".".join(map(str, self.moxa_remote_io.lan_ip)))
                self._ui.lbl_remoteio_firmware.setText(self.moxa_remote_io.firmware_version)
                self._ui.lbl_remoteio_model_name.setText(self.moxa_remote_io.model_name)
                self._ui.lbl_remoteio_connection_status.setText("Connected")

                self.remote_io_table = IODrivesTable(self._ui.tbl_DIO_drives, self.moxa_remote_io)
                self.remote_io_table.set_report_manager(self._report_manager)
            else:
                logger.error("Moxa E1242 Remote IO not detected")
                self._ui.lbl_remoteio_connection_status.setText("Not connected")
                self.moxa_remote_io = None

        else:
            self._ui.lbl_remoteio_ip.setText("-")
            self._ui.lbl_remoteio_firmware.setText("-")
            self._ui.lbl_remoteio_model_name.setText("-")
            self._ui.lbl_remoteio_connection_status.setText("disabled")

        min_sw_version_slewing = self.settings.value("min_sw_version_slewing", "v1.25")
        min_sw_version_lift = self.settings.value("min_sw_version_lift", "v3.16")
        max_error_current_slewing = self.settings.value("max_error_current_slewing", 600)
        max_error_current_lift = self.settings.value("max_error_current_lift", 800)
        block_duration = self.settings.value("block_duration", 4)

        # init min sw version to UI
        self._ui.led_min_sw_ver_slewing.setText(min_sw_version_slewing)
        self._ui.led_min_sw_ver_lift.setText(min_sw_version_lift)
        self._ui.spb_max_slewing_current.setValue(int(max_error_current_slewing))
        self._ui.spb_max_lift_current.setValue(int(max_error_current_lift))
        self._ui.spb_block_duration.setValue(int(block_duration))

        # Signals for min software version
        self._ui.led_min_sw_ver_slewing.editingFinished.connect(self.on_settings_edited)
        self._ui.led_min_sw_ver_lift.editingFinished.connect(self.on_settings_edited)
        # Signals for max current error
        self._ui.spb_max_slewing_current.editingFinished.connect(self.on_settings_edited)
        self._ui.spb_max_lift_current.editingFinished.connect(self.on_settings_edited)
        self._ui.spb_block_duration.editingFinished.connect(self.on_settings_edited)

        self._ui.led_print_label_with_serial.setFocus()  # set focus automatically on label serial number to print
        self._ui.led_print_label_with_serial.returnPressed.connect(self.on_print_label)
        self._ui.lbl_print_lbl_detection_status.setText("")

        # init menuBar actions
        def action_settings():
            settings_diag = SettingsDialog()

        def action_Label_Printer():
            label_printer_dialog = LabelPrinterDialog()

        self._ui.actionSettings.triggered.connect(action_settings)
        self._ui.actionLabel_Printer.triggered.connect(action_Label_Printer)
        self._ui.actionExit.triggered.connect(self.close)

        self.show()

    def closeEvent(self, event):

        # Create the QMessageBox instance manually
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Confirmation')
        msg_box.setText('Do you really want to close the application?')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # Show the message box and capture the user's response
        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            if self.moxa_remote_io is not None:
                self.moxa_remote_io.stop()
                del self.moxa_remote_io
            event.accept()
        else:
            event.ignore()

    def on_print_label(self) -> None:
        """
        Print label method, will display serial number found on label and clear Text edit automatically for next input
        :return:
        """
        serial = self._ui.led_print_label_with_serial.text()
        logger.debug(f"Print label command detected for serial number {serial}")

        if self.node_table is None:
            return

        ret = self.node_table.report_manager.print_label_from_serial_number(serial)
        if ret == 0:
            self._ui.lbl_print_lbl_detection_status.setText("No label to print detected")
        else:
            self._ui.lbl_print_lbl_detection_status.setText(f"Label SN: {ret}")

        QTimer.singleShot(1000, self._ui.led_print_label_with_serial.clear)  # clear text edit widget
        QTimer.singleShot(3000, self._ui.lbl_print_lbl_detection_status.clear)  # clear label widget

    def on_settings_edited(self):
        lne = self.sender()
        lneName = lne.objectName()

        if lne == self._ui.led_min_sw_ver_lift:
            self.settings.setValue("min_sw_version_lift", lne.text())

        if lne == self._ui.led_min_sw_ver_slewing:
            self.settings.setValue("min_sw_version_slewing", lne.text())

        if lne == self._ui.spb_max_lift_current:
            self.settings.setValue("max_error_current_lift", lne.value())

        if lne == self._ui.spb_max_slewing_current:
            self.settings.setValue("max_error_current_slewing", lne.value())

        if lne == self._ui.spb_block_duration:
            self.settings.setValue("block_duration", lne.value())

        self._ui.led_print_label_with_serial.setFocus()  # switch focus automatically to serial to print

        logger.debug(f'{lneName} modified to {lne.text()}')
