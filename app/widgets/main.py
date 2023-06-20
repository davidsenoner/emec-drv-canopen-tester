import logging

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView

from app.widgets.ui_main import Ui_MainWindow

from app.widgets.node_table import NodeTable
from app.modules.network_manager import NetworkManager

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
        self.setWindowTitle("EMEC Drive End-Of-Line Tester v1.4")  # Window title bar

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

        self.show()
