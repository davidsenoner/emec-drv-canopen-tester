import logging

from canopen import Network
import os

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor

from app.widgets.ui_main import Ui_MainWindow

from app.widgets.node_table import NodeTable
from app.widgets.scanner_table import ScannerTable
from app.modules.network_manager import NetworkManager

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)-11s - %(levelname)-7s - %(message)s",
)

channel = 'can0'
baud = 125000
bus_type = 'socketcan'


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Init UI
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

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
            self.scanner_table = ScannerTable(self._ui.tbl_available_nodes, self.network_manager.network_list)
            self.node_table = NodeTable(self._ui.tbl_node_list, self.network_manager.network_list)

            # Connect Qt Signals
            self._ui.btn_detect_nodes.clicked.connect(self.scanner_table.search)
            self.scanner_table.nodes_changed.connect(self.node_table.update_node_table_rows)
            self.node_table.nodes_changed.connect(self.scanner_table.draw_table)

        self.show()
