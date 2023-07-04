import logging

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView

from app.widgets.ui_main import Ui_MainWindow

from app.widgets.node_table import NodeTable
from app.modules.network_manager import NetworkManager

from PyQt5.QtCore import QSettings

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)-11s - %(levelname)-7s - %(message)s",
)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Init UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.showMaximized()
        self.setWindowTitle("EMEC Drive End-Of-Line Tester v2.0.0")  # Window title bar

        # Init canopen logger
        logging.getLogger('can').setLevel(logging.ERROR)
        logging.getLogger('canopen').setLevel(logging.ERROR)

        # Init default widgets
        network_status_list = [
            self._ui.lbl_can0_status,
            self._ui.lbl_can1_status,
            self._ui.lbl_can2_status,
            self._ui.lbl_can3_Status
        ]

        for label in network_status_list:
            label.setText("No connection")

        self.network_manager = NetworkManager()

        if len(self.network_manager.network_list) > 0:

            # Print bus status
            for label, network in enumerate(self.network_manager.network_list):
                network_status_list[label].setText(network.bus.channel_info)

            # Init Tables
            self.node_table = NodeTable(self._ui.tbl_node_list, self.network_manager.network_list)

        # Settings management
        self.settings = QSettings("EMEC", "Tester")

        min_sw_version_slewing = self.settings.value("min_sw_version_slewing", "v1.25")
        min_sw_version_lift = self.settings.value("min_sw_version_lift", "v3.16")

        # init min sw version to UI
        self._ui.led_min_sw_ver_slewing.setText(min_sw_version_slewing)
        self._ui.led_min_sw_ver_lift.setText(min_sw_version_lift)

        # Signals for min software version
        self._ui.led_min_sw_ver_lift.editingFinished.connect(self.update_qsettings)
        self._ui.led_min_sw_ver_slewing.editingFinished.connect(self.update_qsettings)

        self.show()

    def update_qsettings(self):
        lne = self.sender()
        lneName = lne.objectName()

        if lne == self._ui.led_min_sw_ver_lift:
            self.settings.setValue("min_sw_version_lift", lne.text())

        if lne == self._ui.led_min_sw_ver_slewing:
            self.settings.setValue("min_sw_version_slewing", lne.text())

        logger.debug(f'{lneName} modified to {lne.text()}')
