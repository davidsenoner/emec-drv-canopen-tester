import logging

from canopen import Network
import os

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor

from app.widgets.ui_main import Ui_MainWindow

from app.widgets.node_table import NodeTable
from app.widgets.scanner_table import ScannerTable

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

        # Init default widgets
        self._ui.lbl_can_status.setText("No connection")

        # Init CANOpen
        os.system(f'sudo ifconfig {channel} down')
        os.system(f'sudo ip link set {channel} type can bitrate {baud}')
        os.system(f"sudo ifconfig {channel} txqueuelen {baud}")
        os.system(f'sudo ifconfig {channel} up')

        # Init Network
        self.network = Network()
        try:
            self.network.connect(channel=channel, bustype=bus_type)
        except Exception as e:
            logging.debug(f'Error during Network Init: {e}')

        if hasattr(self.network.bus, "channel"):
            # Print bus status
            self._ui.lbl_can_status.setText(self.network.bus.channel_info)

            # Init Tables
            self.scanner_table = ScannerTable(self._ui.tbl_available_nodes, self.network)
            self.node_table = NodeTable(self._ui.tbl_node_list, self.network)

            # Connect Qt Signals
            self._ui.btn_detect_nodes.clicked.connect(self.scanner_table.search)
            self.scanner_table.nodes_changed.connect(self.node_table.draw_table)
            self.node_table.nodes_changed.connect(self.scanner_table.draw_table)

        self.show()
