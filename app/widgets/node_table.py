import logging
import time
from canopen import Network, BaseNode402

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QHeaderView, QTableWidget, QMenu, QMessageBox
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QCursor

from app.modules.emecdrv_tester import EMECDrvTester

logger = logging.getLogger(__name__)


class NodeTableRow(EMECDrvTester):
    def __init__(self, network: Network, channel: int, node: BaseNode402):
        super().__init__(node)
        self._network = network
        self._channel = channel
        self._node = node

    @property
    def network(self) -> Network:
        return self._network

    @network.setter
    def network(self, value: Network):
        self._network = value

    @property
    def channel(self) -> int:
        return self._channel

    @channel.setter
    def channel(self, value: int):
        self._channel = value

    @property
    def node_id(self) -> int:
        return self._node.id

    @property
    def node(self) -> BaseNode402:
        return self._node

    @node.setter
    def node(self, value):
        self._node = value


class NodeTable(QObject):
    nodes_changed = pyqtSignal(int)

    def __init__(self,
                 widget: QTableWidget,
                 networks: list
                 ):
        super().__init__()

        self.table_widget = widget
        self.networks = networks
        self.table_rows = {}

        _headers = [
            "Channel",
            "Node ID",
            "Start",
            "Stop",
            "CW",
            "CCW",
            "Pos",
            "Duration",
            "min/max time",
            "State",
        ]

        self.table_widget.setColumnCount(len(_headers))
        self.table_widget.setHorizontalHeaderLabels(_headers)
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.on_context_menu)

        self.refresh_table_timer = QTimer()
        self.refresh_table_timer.start(10000)
        self.refresh_table_timer.timeout.connect(self.draw_node_info)

        self.draw_table()

    @staticmethod
    def start_node(node_table_row: NodeTableRow):
        try:
            node_table_row.start_test()
        except Exception as e:
            logger.debug(f'Error during start test command: {e}')
            return

    @staticmethod
    def stop_node(node_table_row: NodeTableRow):
        try:
            node_table_row.stop_test()
        except Exception as e:
            logger.debug(f'Error during stop test command: {e}')

    @staticmethod
    def reset_node(node_table_row: NodeTableRow):
        try:
            node_table_row.ack_error()
        except Exception as e:
            logger.debug(f'Error during Ack command: {e}')
        logger.debug(f'Reset Node ID: {node_table_row.node_id} by user')

    @staticmethod
    def pop_node(node_table_row: NodeTableRow):
        try:
            # Pop node from network
            if node_table_row.node_id in node_table_row.network:
                node_table_row.network.pop(node_table_row.node_id)
            time.sleep(0.05)
        except Exception as e:
            logger.debug(f'Error removing node from network: {e}')

    def update_node_table_rows(self):
        for channel, network in enumerate(self.networks):
            if network is None:
                continue

            for node_id in network:
                key = f'{channel}_{node_id}'

                if key not in self.table_rows:
                    try:
                        node_table_row = NodeTableRow(network=network, channel=channel, node=network.nodes[node_id])
                        node_table_row.failure.connect(self.draw_node_info)
                        node_table_row.started.connect(self.draw_node_info)
                        node_table_row.stopped.connect(self.draw_node_info)
                        node_table_row.test_timer_timeout.connect(self.draw_test_info)

                        self.table_rows.update({key: node_table_row})

                    except Exception as e:
                        logger.debug(e)

        self.draw_table()

    def draw_node_info(self):

        i = 0

        for key, node_table_row in self.table_rows.items():
            # COLUMN CW MOVEMENTS
            _column = 4
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.cw_movements)))

            # COLUMN CCW MOVEMENTS
            _column = 5
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.ccw_movements)))

            # COLUMN MIN/MAX TIME
            _column = 8
            self.table_widget.setItem(i, _column,
                                      QTableWidgetItem(f'{node_table_row.min_time}/{node_table_row.max_time}s'))

            # COLUMN STATUS
            _column = 9
            self.table_widget.setItem(i, _column, QTableWidgetItem(node_table_row.status))

            i += 1

    def draw_test_info(self):

        i = 0

        for key, node_table_row in self.table_rows.items():
            # COLUMN ACTUAL POSITION
            _column = 6
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.actual_position)))

            # COLUMN DURATION
            _column = 7
            seconds = node_table_row.get_elapsed_time()
            duration = str(seconds // 60) + "m " + str(seconds % 60) + "s"
            self.table_widget.setItem(i, _column, QTableWidgetItem(duration))

            i += 1

    def draw_table(self):
        rows = self.table_widget.rowCount()

        # clear table
        for i in reversed(range(rows)):
            self.table_widget.removeRow(i)

        for key, node_table_row in self.table_rows.items():
            i = self.table_widget.rowCount()

            self.table_widget.insertRow(i)
            self.table_widget.setRowHeight(i, 35)

            _column = 0

            # COLUMN CHANNEL
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(key)))

            # COLUMN NODE ID
            _column = 1
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.node_id)))

            # COLUMN START BUTTON
            _column = 2
            btn_start = QPushButton('Start')
            btn_start.setMaximumSize(QSize(50, 30))
            btn_start.setCursor(QCursor(Qt.PointingHandCursor))
            btn_start.clicked.connect(
                lambda arg, n=node_table_row: self.start_node(n)
            )
            self.table_widget.setCellWidget(i, _column, btn_start)

            # COLUMN STOP BUTTON
            _column = 3
            btn_stop = QPushButton('Stop')
            btn_stop.setMaximumSize(QSize(50, 30))
            btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
            btn_stop.clicked.connect(
                lambda arg, n= node_table_row: self.stop_node(n)
            )
            self.table_widget.setCellWidget(i, _column, btn_stop)

            # COLUMN CW MOVEMENTS
            _column = 4
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.cw_movements)))

            # COLUMN CCW MOVEMENTS
            _column = 5
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.ccw_movements)))

            # COLUMN ACTUAL POSITION
            _column = 6
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.actual_position)))

            # COLUMN DURATION
            _column = 7
            seconds = node_table_row.get_elapsed_time()
            duration = str(seconds // 60) + "m " + str(seconds % 60) + "s"
            self.table_widget.setItem(i, _column, QTableWidgetItem(duration))

            # COLUMN MIN/MAX TIME
            _column = 8
            self.table_widget.setItem(i, _column,
                                      QTableWidgetItem(f'{node_table_row.min_time}/{node_table_row.max_time}s'))

            # COLUMN STATUS
            _column = 9
            self.table_widget.setItem(i, _column, QTableWidgetItem(node_table_row.status))

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def on_context_menu(self, pos):
        index = self.table_widget.indexAt(pos)

        if not index.isValid():
            return

        row = index.row()

        key = self.table_widget.item(row, 0).text()  # Column 0 have unique key for channel/node_id

        node_table_row = self.table_rows[key]

        menu = QMenu()

        reset_action = menu.addAction("Reset device")
        remove_safety_action = menu.addAction("Remove safety")
        info_action = menu.addAction("Info")

        action = menu.exec_(self.table_widget.mapToGlobal(pos))

        if action == reset_action:
            self.reset_node(node_table_row)
            self.draw_table()

        if action == remove_safety_action:
            self.pop_node(node_table_row)
            self.table_rows.pop(key)

            # Redraw Tables
            self.draw_table()
            self.nodes_changed.emit(node_table_row.node_id)
            logger.debug(f'Pop Node ID: {node_table_row.node_id} from network: {node_table_row.network}')

        if action == info_action:
            logger.debug(f'Info for Node {node_table_row.node_id}')
            # Create QMessageBox-Dialog

            text = f"Node ID: {node_table_row.node_id}\n"
            text += f"Channel: {node_table_row.channel}\n"
            text += f"Manufacturer Device Name: {node_table_row.manufacturer_device_name}\n"
            text += f"Manufacturer Hardware Version: {node_table_row.manufacturer_hardware_version}\n"
            text += f"Manufacturer Software Version: {node_table_row.manufacturer_software_version}\n"
            text += f"CW/CCW movements: {str(node_table_row.cw_movements)}/{str(node_table_row.ccw_movements)}\n"
            text += f"Accumulative operating time: {str(node_table_row.accumulative_operating_time)}\n"
            text += f"Device temperature: {str(node_table_row.device_temp)} (max: {str(node_table_row.max_device_temp)})\n"
            text += f"State: {str(node_table_row.node.state)}\n"
            text += f"Actual position: {str(node_table_row.actual_position)}\n"
            text += f"Target position: {str(node_table_row.target_position)}\n"
            text += f"Control Word: {hex(node_table_row.control_word)}\n"
            text += f"Status Word: {hex(node_table_row.status_word)}\n"
            text += f"Actual current: {str(node_table_row.current_actual_value)}\n"
            text += f"Rated/Max current: {str(node_table_row.rated_current)}/{str(node_table_row.max_current)}\n"

            msg_box = QMessageBox()
            msg_box.setText(text)
            msg_box.setWindowTitle(f'Info Node {node_table_row.node_id}')
            msg_box.setStandardButtons(QMessageBox.Ok)

            result = msg_box.exec_()
