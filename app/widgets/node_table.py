import logging
import time
from canopen import Network

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView, QTableWidget, QMenu
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QCursor

from app.modules.emecdrv_tester import EMECDrvTester

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

        self.device_list = {}

        _headers = [
            "Node ID",
            "Start",
            "Stop",
            "CW",
            "CCW",
            "Pos",
            "Duration",
            "State"
        ]

        self.table_widget.setColumnCount(len(_headers))
        self.table_widget.setHorizontalHeaderLabels(_headers)
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.on_context_menu)

        self.refresh_table_timer = QTimer()
        self.refresh_table_timer.start(10000)
        self.refresh_table_timer.timeout.connect(self.draw_node_info)

        self.draw_table()

    def draw_table(self):
        rows = self.table_widget.rowCount()
        ccw_movements = 0
        cw_movements = 0
        state = ""
        duration = 0
        position = 0

        # clear table
        for i in reversed(range(rows)):
            self.table_widget.removeRow(i)

        for node_id in self.network:
            try:
                node = self.network.nodes[node_id]  # Get node from ID
                #state = node.state  # get state
                ccw_movements = node.sdo[0x2000][1].raw
                cw_movements = node.sdo[0x2000][2].raw

                if node_id in self.device_list:
                    state = self.device_list[node_id].status
                    position = self.device_list[node_id].actual_position
                    seconds = self.device_list[node_id].get_elapsed_time()
                    duration = str(seconds // 60) + "m " + str(seconds % 60) + "s"
                else:
                    state = "Idle"

            except Exception as e:
                logger.debug(f"Error during reading of node: {e}")

            i = self.table_widget.rowCount()

            self.table_widget.insertRow(i)
            self.table_widget.setRowHeight(i, 35)

            _column = 0

            # COLUMN NODE ID
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_id)))

            # COLUMN START BUTTON
            _column = 1
            btn_start = QPushButton('Start')
            btn_start.setMaximumSize(QSize(50, 30))
            btn_start.setCursor(QCursor(Qt.PointingHandCursor))
            btn_start.clicked.connect(lambda state=False, j=node_id: self.start_node(j))
            self.table_widget.setCellWidget(i, _column, btn_start)

            # COLUMN STOP BUTTON
            _column = 2
            btn_stop = QPushButton('Stop')
            btn_stop.setMaximumSize(QSize(50, 30))
            btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
            btn_stop.clicked.connect(lambda state=False, j=node_id: self.stop_node(j))
            self.table_widget.setCellWidget(i, _column, btn_stop)

            # COLUMN CW MOVEMENTS
            _column = 3
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(cw_movements)))

            # COLUMN CCW MOVEMENTS
            _column = 4
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(ccw_movements)))

            # COLUMN ACTUAL POSITION
            _column = 5
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(position)))

            # COLUMN DURATION
            _column = 6
            self.table_widget.setItem(i, _column, QTableWidgetItem(duration))

            # COLUMN STATUS
            _column = 7
            self.table_widget.setItem(i, _column, QTableWidgetItem(state))

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def draw_test_info(self):
        duration = 0
        position = 0

        for i, node_id in enumerate(self.network):
            if node_id in self.device_list:
                position = self.device_list[node_id].actual_position
                seconds = self.device_list[node_id].get_elapsed_time()
                duration = str(seconds // 60) + "m " + str(seconds % 60) + "s"

            # COLUMN ACTUAL POSITION
            _column = 5
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(position)))

            # COLUMN DURATION
            _column = 6
            self.table_widget.setItem(i, _column, QTableWidgetItem(duration))

    def draw_node_info(self):

        ccw_movements = 0
        cw_movements = 0
        state = ""

        for i, node_id in enumerate(self.network):
            try:
                node = self.network.nodes[node_id]  # Get node from ID
                #state = node.state  # get state
                ccw_movements = node.sdo[0x2000][1].raw
                cw_movements = node.sdo[0x2000][2].raw

                if node_id in self.device_list:
                    state = self.device_list[node_id].status
                else:
                    state = "Idle"

            except Exception as e:
                logger.debug(f"Error during reading of node: {e}")

            # COLUMN CW MOVEMENTS
            _column = 3
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(cw_movements)))

            # COLUMN CCW MOVEMENTS
            _column = 4
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(ccw_movements)))

            # COLUMN STATUS
            _column = 7
            self.table_widget.setItem(i, _column, QTableWidgetItem(state))

    def on_context_menu(self, pos):
        index = self.table_widget.indexAt(pos)
        row = index.row()

        column = 0  # Columns of Node ID specified in draw_table

        item = self.table_widget.item(row, column)
        node_id = int(item.text())  # Cell contains the node id as string

        if not index.isValid():
            return

        menu = QMenu()

        reset_action = menu.addAction("Reset device")
        remove_safety_action = menu.addAction("Remove safety")
        info_action = menu.addAction("Info")

        action = menu.exec_(self.table_widget.mapToGlobal(pos))

        if action == reset_action:
            self.reset_node(node_id)

        if action == remove_safety_action:
            self.pop_node(node_id)

        if action == info_action:
            logger.debug(f'Info for Node {node_id}')

    def start_node(self, node_id: int):
        try:
            if node_id not in self.device_list:
                node = self.network.nodes[node_id]
                self.device_list.update({node_id: EMECDrvTester(node=node)})

            device = self.device_list[node_id]

            device.initialised.connect(self.draw_table)

            device.failure.connect(self.draw_node_info)
            device.started.connect(self.draw_node_info)
            device.stopped.connect(self.draw_node_info)
            device.test_timer_timeout.connect(self.draw_test_info)

            device.start_test()

        except Exception as e:
            logger.debug(e)
            return

    def stop_node(self, node_id: int):
        if node_id in self.device_list:
            device = self.device_list[node_id]
            try:
                device.stop_test()
            except Exception as e:
                logger.debug(f'Error during stop test command: {e}')

    def reset_node(self, node_id: int):
        if node_id in self.device_list:
            try:
                device = self.device_list[node_id]
                device.ack_error()
            except Exception as e:
                logger.debug(f'Error during Ack command: {e}')

        self.draw_table()
        logger.debug(f'Reset Node ID: {node_id}')

    def pop_node(self, node_id: int):

        if node_id in self.device_list:
            if self.device_list[node_id].isActive():  # if timer active stop test first
                self.device_list[node_id].stop_test()
            self.device_list.pop(node_id)

        # Pop node from network
        if node_id in self.network:
            self.network.pop(node_id)
        time.sleep(0.05)

        # Redraw Tables
        self.draw_table()
        self.nodes_changed.emit(node_id)
        logger.debug(f'Pop Node ID: {node_id}')
