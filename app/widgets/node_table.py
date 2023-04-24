import logging
import time
from canopen import Network

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView, QTableWidget
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QCursor

from app.modules.lift_tester import LiftTester

logger = logging.getLogger(__name__)


class NodeTable(QObject):
    nodes_changed = pyqtSignal(int)
    def __init__(self,
                 widget: QTableWidget,
                 network: Network
                 ):
        super().__init__()

        self.table_widget = widget
        self.network = network

        self.tester_list = {}

        _headers = [
            "Node ID",
            "Start",
            "Stop",
            "Reset",
            "Remove",
            "State",
            "NMT State"
        ]

        self.table_widget.setColumnCount(len(_headers))
        self.table_widget.setHorizontalHeaderLabels(_headers)

        self.draw_table()

    def draw_table(self):
        rows = self.table_widget.rowCount()

        # clear table
        for i in reversed(range(rows)):
            self.table_widget.removeRow(i)

        for node_id in self.network:

            node = self.network.nodes[node_id]  # Get node from ID
            i = self.table_widget.rowCount()

            self.table_widget.insertRow(i)
            self.table_widget.setRowHeight(i, 35)

            _column = 0

            # COLUMN NODE ID
            self.table_widget.setItem(i, _column, QTableWidgetItem(f'ID: {node_id}'))

            # COLUMN START BUTTON
            _column = _column + 1
            btn_start = QPushButton('Start')
            btn_start.setMaximumSize(QSize(50, 30))
            btn_start.setCursor(QCursor(Qt.PointingHandCursor))
            btn_start.clicked.connect(lambda state=False, j=node_id: self.start_node(j))
            self.table_widget.setCellWidget(i, _column, btn_start)

            # COLUMN STOP BUTTON
            _column = _column + 1
            btn_stop = QPushButton('Stop')
            btn_stop.setMaximumSize(QSize(50, 30))
            btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
            btn_stop.clicked.connect(lambda state=False, j=node_id: self.stop_node(j))
            self.table_widget.setCellWidget(i, _column, btn_stop)

            # COLUMN RESET BUTTON
            _column = _column + 1
            btn_stop = QPushButton('Reset')
            btn_stop.setMaximumSize(QSize(60, 30))
            btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
            btn_stop.clicked.connect(lambda state=False, j=node_id: self.reset_node(j))
            self.table_widget.setCellWidget(i, _column, btn_stop)

            # COLUMN REMOVE BUTTON
            _column = _column + 1
            btn_stop = QPushButton('Remove')
            btn_stop.setMaximumSize(QSize(60, 30))
            btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
            btn_stop.clicked.connect(lambda state=False, j=node_id: self.pop_node(j))
            self.table_widget.setCellWidget(i, _column, btn_stop)

            # COLUMN STATUS
            _column = _column + 1
            state = node.state  # get state
            self.table_widget.setItem(i, _column, QTableWidgetItem(state))

            # COLUMN NMT STATUS
            _column = _column + 1
            state = node.nmt.state  # get state
            self.table_widget.setItem(i, _column, QTableWidgetItem(state))

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def start_node(self, node_id: int):

        if node_id not in self.tester_list:
            node = self.network.nodes[node_id]
            self.tester_list.update({node_id: LiftTester(node=node)})

        tester = self.tester_list[node_id]
        tester.start_test()

    def stop_node(self, node_id: int):
        if node_id in self.tester_list:
            tester = self.tester_list[node_id]
            tester.stop_test()

    def reset_node(self, node_id: int):

        self.init_node(node_id=node_id)
        self.draw_table()
        logger.debug(f'Reset Node ID: {node_id}')

    def pop_node(self, node_id: int):

        # Pop node from network
        self.network.pop(node_id)
        time.sleep(0.05)

        # Redraw Tables
        self.draw_table()
        self.nodes_changed.emit(node_id)
        logger.debug(f'Pop Node ID: {node_id}')

    def init_node(self, node_id: int):

        node = self.network.nodes[node_id]  # Get node from ID

        node.nmt.state = 'OPERATIONAL'

        node.sdo[0x6060].raw = 0x01  # “Profile Position” operating mode

        node.sdo[0x6040].raw = 0x06
        node.sdo[0x6040].raw = 0x07
        node.sdo[0x6040].raw = 0x0F

        if node.state == 'FAULT':
            node.sdo[0x6040].raw = node.sdo[0x6040].raw | 0x80

