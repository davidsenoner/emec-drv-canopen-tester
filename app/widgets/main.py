import logging

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

from app.widgets.ui_main import Ui_MainWindow

from app.widgets.node_table import NodeTable
from app.modules.network_manager import NetworkManager
from app.widgets.settings_dialog import SettingsDialog

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

        # Init UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.showMaximized()
        self.setWindowTitle(f"EMEC Drive End-Of-Line Tester {version}")  # Window title bar
        self.node_table = None

        self.network_manager = NetworkManager()

        self._ui.lbl_detected_cahnnels.setText(f"{len(self.network_manager.network_list)} channels")

        if len(self.network_manager.network_list) > 0:  # at least ne channel detected
            self.node_table = NodeTable(self._ui.tbl_node_list, self.network_manager.network_list)  # Init Tables

        # Settings management
        self.settings = QSettings("EMEC", "Tester")

        min_sw_version_slewing = self.settings.value("min_sw_version_slewing", "v1.25")
        min_sw_version_lift = self.settings.value("min_sw_version_lift", "v3.16")
        max_error_current_slewing = self.settings.value("max_error_current_slewing", 600)
        max_error_current_lift = self.settings.value("max_error_current_lift", 800)
        block_current_threshold = self.settings.value("block_current_threshold", 1500)

        # init min sw version to UI
        self._ui.led_min_sw_ver_slewing.setText(min_sw_version_slewing)
        self._ui.led_min_sw_ver_lift.setText(min_sw_version_lift)
        self._ui.spb_max_slewing_current.setValue(int(max_error_current_slewing))
        self._ui.spb_max_lift_current.setValue(int(max_error_current_lift))
        self._ui.spb_blocked_current_thr_slewing.setValue(int(block_current_threshold))

        # Signals for min software version
        self._ui.led_min_sw_ver_slewing.editingFinished.connect(self.on_settings_edited)
        self._ui.led_min_sw_ver_lift.editingFinished.connect(self.on_settings_edited)
        # Signals for max current error
        self._ui.spb_max_slewing_current.editingFinished.connect(self.on_settings_edited)
        self._ui.spb_max_lift_current.editingFinished.connect(self.on_settings_edited)
        self._ui.spb_blocked_current_thr_slewing.editingFinished.connect(self.on_settings_edited)

        self._ui.led_print_label_with_serial.setFocus()  # set focus automatically on label serial number to print
        self._ui.led_print_label_with_serial.returnPressed.connect(self.on_print_label)
        self._ui.lbl_print_lbl_detection_status.setText("")

        # init menuBar actions
        def action_settings():
            settings_diag = SettingsDialog()

        self._ui.actionSettings.triggered.connect(action_settings)

        self.show()

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

        if lne == self._ui.spb_blocked_current_thr_slewing:
            self.settings.setValue("block_current_threshold", lne.value())

        self._ui.led_print_label_with_serial.setFocus()  # switch focus automatically to serial to print

        logger.debug(f'{lneName} modified to {lne.text()}')
