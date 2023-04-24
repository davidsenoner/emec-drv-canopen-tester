import logging
import time
from canopen import Network
from canopen.profiles.p402 import BaseNode402

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView, QTableWidget
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QCursor

logger = logging.getLogger(__name__)


TITAN40_EMECDRV5_LIFT_NODE_ID = 0x0C
TITAN40_EMECDRV5_SLEWING_NODE_ID = 0x0D


class ScannerTable(QObject):
    nodes_changed = pyqtSignal(int)
    def __init__(self,
                 widget: QTableWidget,
                 network: Network
                 ):
        super().__init__()

        self.table_widget = widget
        self.network = network

        _headers = [
            "Node ID",
            "Type",
            "Add Node",
            "Added"
        ]

        self.table_widget.setColumnCount(len(_headers))
        self.table_widget.setHorizontalHeaderLabels(_headers)

        # Init Scanner
        self.network.scanner.search()

        self.draw_table()

    def search(self):
        self.network.scanner.reset()
        self.network.scanner.search()
        time.sleep(0.05)
        self.draw_table()

    def draw_table(self):
        rows = self.table_widget.rowCount()

        # clear table
        for i in reversed(range(rows)):
            self.table_widget.removeRow(i)

        for node_id in self.network.scanner.nodes:
            i = self.table_widget.rowCount()

            self.table_widget.insertRow(i)
            self.table_widget.setRowHeight(i, 35)

            _column = 0

            # COLUMN NODE ID
            self.table_widget.setItem(i, _column, QTableWidgetItem(f'ID: {node_id}'))

            # COLUMN NODE TYPE
            _column = _column + 1
            if node_id == TITAN40_EMECDRV5_LIFT_NODE_ID:
                self.table_widget.setItem(i, _column, QTableWidgetItem(f'Lift'))
            elif node_id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
                self.table_widget.setItem(i, _column, QTableWidgetItem(f'Slewing'))
            else:
                self.table_widget.setItem(i, _column, QTableWidgetItem(f'Unknown'))

            # COLUMN ADD NODE BUTTON
            _column = _column + 1
            btn_start = QPushButton('Add')
            btn_start.setMaximumSize(QSize(50, 30))
            btn_start.setCursor(QCursor(Qt.PointingHandCursor))
            btn_start.clicked.connect(lambda state=False, j=node_id: self.add_node(j))
            self.table_widget.setCellWidget(i, _column, btn_start)

            # COLUMN NODE ADDED
            _column = _column + 1
            if node_id in self.network.nodes:
                self.table_widget.setItem(i, _column, QTableWidgetItem(f'OK'))
            else:
                self.table_widget.setItem(i, _column, QTableWidgetItem(f'NOK'))

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def add_node(self, node_id: int):
        # Create node from ID
        new_node = BaseNode402(node_id, 'app/resources/eds/emecdrv5.eds')

        # Add new node to network
        self.network.add_node(new_node)
        logging.debug(f'Node ID {node_id} added to network')

        # Redraw tables
        time.sleep(0.05)
        self.draw_table()
        self.nodes_changed.emit(new_node.id)
