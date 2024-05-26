import logging
import time
import platform
from canopen import Network, BaseNode402

from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHeaderView, QTableWidget, QMenu, QMessageBox
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject, QTimer, QSettings
from PyQt5.QtGui import QCursor, QColor, QBrush

from app.modules.emecdrv_tester import EMECDrvTester
from app.modules.emecdrv_tester import TITAN40_EMECDRV5_SLEWING_NODE_ID, TITAN40_EMECDRV5_LIFT_NODE_ID
from app.widgets.add_info_diag import AddInfoDialog
from app.widgets.add_sn_diag import AddSNDialog
from app.modules.test_report import Label, TestReportManager, keep_latest_files

logger = logging.getLogger(__name__)


def get_label_temp_folder():
    os = platform.system()
    if os == "Windows":
        return "C:/tmp/labels/"
    else:
        return "/var/tmp/labels/"


class NodeTableRow(EMECDrvTester):
    label_present_signal = pyqtSignal(Label)

    def __init__(self, network: Network, channel: int, node: BaseNode402):
        super().__init__(node)

        self._network = network
        self._channel = channel
        self._node = node
        self._serial_number = 0
        self._customer = ""
        self._comment = ""
        self._report = None

        self.generate_label_signal.connect(self.on_label_present)

    def __str__(self):
        if self.node.id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            return f"Slewing"
        elif self.node.id == TITAN40_EMECDRV5_LIFT_NODE_ID:
            return f"Lift"
        else:
            return f"Unknown"

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

    @property
    def serial_number(self) -> int:
        return self._serial_number

    @serial_number.setter
    def serial_number(self, sn: int) -> None:
        self._serial_number = sn

    @property
    def customer(self) -> str:
        return self._customer

    @customer.setter
    def customer(self, customer: str) -> None:
        self._customer = customer

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment: str) -> None:
        self._comment = comment

    def on_label_present(self):
        """
        Create a label and send a signal passing the label
        This method should be connected to a singnal (es. timeout signal)
        :return:
        """
        logger.debug(f"Create Label for serial number {self.serial_number}")
        label = Label(self.serial_number)
        label.node_id = self.node_id
        label.mean_current = self.current_stat.mean()
        label.type = str(self)

        self.label_present_signal.emit(label)


class NodeTable(QObject):
    def __init__(self, widget: QTableWidget, networks: list):
        super().__init__()

        self._start_node_id = []
        self.table_widget = widget
        self.networks = networks
        self.table_rows = {}
        self._redraw_table = True

        self.settings = QSettings("EMEC", "Tester")
        self._headers = ["Ch_Id", "Type", "Start", "Stop", "CW", "CCW", "Pos", "Duration", "Current", "SW-Version",
                         "Serial number", "State", "Test mode"]

        self.table_widget.setColumnCount(len(self._headers))
        self.table_widget.setHorizontalHeaderLabels(self._headers)
        self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.on_context_menu)
        self.table_widget.horizontalHeader().setContentsMargins(10, 0, 10, 0)

        self.refresh_table_timer = QTimer()
        self.refresh_table_timer.start(1000)
        self.refresh_table_timer.timeout.connect(self.refresh)

        self.refresh_table_timer1 = QTimer()
        self.refresh_table_timer1.start(800)
        self.refresh_table_timer1.timeout.connect(self.draw_table)

        layout = self.get_layout_settings()
        label_temp_folder = get_label_temp_folder()

        settings = QSettings("EMEC", "Tester")
        max_labels = settings.value("label_files_cache", 50, type=int)
        keep_latest_files(label_temp_folder, max_labels)

        self._report_manager = TestReportManager(label_temp_folder, **layout)

    def get_layout_settings(self):
        return {
            "columns": self.settings.value("label_paper_columns", 2, type=int),
            "column_width": self.settings.value("label_column_width", 60, type=int),
            "column_height": self.settings.value("label_column_height", 30, type=int),
            "top_padding": self.settings.value("label_column_top", 8, type=int),
            "bottom_padding": self.settings.value("label_column_bottom", 8, type=int),
            "left_padding": self.settings.value("label_column_left", 10, type=int),
            "right_padding": self.settings.value("label_column_right", 10, type=int),
        }

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
            node_table_row.stop_test("Stopped by user")
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
    def pop_node(node_table_row):
        try:
            # Pop node from network
            if node_table_row.node_id in node_table_row.network:
                node_table_row.network.pop(node_table_row.node_id)
            time.sleep(0.05)
        except Exception as e:
            logger.error(f'Error removing node from network: {e}')

    @staticmethod
    def add_node(network: Network, node_id: int):
        # Create node from ID
        try:
            eds = 'app/resources/eds/emecdrv5.eds'
            # Add new node to network
            network.add_node(BaseNode402(node_id, eds))
            time.sleep(0.05)
            logging.debug(f'Node ID {node_id} added to network using EDS: {eds}')
        except Exception as e:
            logger.error(f'Error when adding node to network: {e}')

    def update_node_table_rows(self):
        for channel, network in enumerate(self.networks):
            if network is None:
                continue

            self.add_new_nodes(channel, network)
            self.remove_absent_nodes(channel, network)

    def add_new_nodes(self, channel, network):
        for node_id in network:
            key = f'{channel}_{node_id}'

            if key not in self.table_rows:
                node_table_row = NodeTableRow(network=network, channel=channel, node=network.nodes[node_id])

                node_table_row.on_test_timer_timeout.connect(self.draw_cyclic_info)
                self.table_rows.update({key: node_table_row})

                if self.settings.value("sn_mnt_active", True, type=bool):
                    dialog = AddSNDialog(channel=channel, node_id=node_id)
                    node_table_row.serial_number = dialog.serial_number
                    node_table_row.label_present_signal.connect(self._report_manager.add_label)

    def remove_absent_nodes(self, channel, network):
        key_to_remove = []
        try:
            key_to_remove = [key for key in self.table_rows if str(key).startswith(f'{channel}_') and int(
                key.replace(f'{channel}_', '', 1)) not in network.scanner.nodes]
        except Exception as e:  # If exception (can happen if transmit buffer full) than remove all nodes
            network.clear()
            logging.debug(f'All Nodes removed from network: {e}')

        for key in key_to_remove:
            row = self.table_rows[key]
            self.report_manager.print_label_from_serial_number(row.serial_number)
            self.pop_node(row)
            self.table_rows.pop(key)
            logging.info(f'Node ID {key} removed')

    def draw_cyclic_info(self):

        i = 0

        for key, node_table_row in self.table_rows.items():

            # COLUMN CW MOVEMENTS
            _column = 4
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.get_cw_movements())))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN CCW MOVEMENTS
            _column = 5
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.get_ccw_movements())))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN ACTUAL POSITION
            _column = 6
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.get_actual_position())))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN DURATION
            _column = 7
            seconds = node_table_row.get_elapsed_time()
            duration = str(seconds // 60) + "m " + str(seconds % 60) + "s"
            self.table_widget.setItem(i, _column, QTableWidgetItem(duration))

            # COLUMN ACTUAL CURRENT
            _column = 8
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(f'{node_table_row.get_actual_current()} mA'))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN STATUS
            _column = 11
            self.table_widget.setItem(i, _column, QTableWidgetItem(node_table_row.get_status()))
            i += 1

            # COLUMN TESTING MODE
            _column = 12
            self.table_widget.setItem(i, _column, QTableWidgetItem(node_table_row.get_test_mode_description()))
            i += 1

            # logger.debug(f"Mean current: {node_table_row.current_stat.mean()}")  # mean current
            # logger.debug(f"Std current: {node_table_row.current_stat.stdev()}")  # standard deviation

    def draw_table(self):

        if not self._redraw_table:
            return

        self._redraw_table = False

        self.update_node_table_rows()

        rows = self.table_widget.rowCount()

        # clear table
        for i in reversed(range(rows)):
            self.table_widget.removeRow(i)

        for key, node_table_row in self.table_rows.items():

            i = self.table_widget.rowCount()

            self.table_widget.insertRow(i)
            self.table_widget.setRowHeight(i, 40)

            _column = 0

            # COLUMN CHANNEL
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(key)))

            # COLUMN NODE TYPE
            _column = 1
            self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row)))

            # COLUMN START BUTTON
            _column = 2
            btn_start = QPushButton('Start')
            btn_start.setMaximumSize(QSize(60, 35))
            btn_start.setCursor(QCursor(Qt.PointingHandCursor))
            btn_start.clicked.connect(
                lambda arg, n=node_table_row: self.start_node(n)
            )
            self.table_widget.setCellWidget(i, _column, btn_start)

            # COLUMN STOP BUTTON
            _column = 3
            btn_stop = QPushButton('Stop')
            btn_stop.setMaximumSize(QSize(60, 35))
            btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
            btn_stop.clicked.connect(
                lambda arg, n=node_table_row: self.stop_node(n)
            )
            self.table_widget.setCellWidget(i, _column, btn_stop)

            # COLUMN CW MOVEMENTS
            _column = 4
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.get_cw_movements())))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN CCW MOVEMENTS
            _column = 5
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.get_ccw_movements())))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN ACTUAL POSITION
            _column = 6
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(str(node_table_row.get_actual_position())))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN DURATION
            _column = 7
            seconds = node_table_row.get_elapsed_time()
            duration = str(seconds // 60) + "m " + str(seconds % 60) + "s"
            self.table_widget.setItem(i, _column, QTableWidgetItem(duration))

            # COLUMN ACTUAL CURRENT
            _column = 8
            try:
                self.table_widget.setItem(i, _column, QTableWidgetItem(f'{node_table_row.get_actual_current()} mA'))
            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN SOFTWARE VERSION
            _column = 9
            try:
                item = QTableWidgetItem(node_table_row.manufacturer_software_version)

                brush = QBrush(QColor(255, 0, 0, 255))
                brush.setStyle(Qt.SolidPattern)

                if node_table_row.get_software_version_ok():
                    item.setForeground(QBrush())
                else:
                    item.setForeground(brush)
                self.table_widget.setItem(i, _column, item)

            except Exception as e:
                self.table_widget.setItem(i, _column, QTableWidgetItem("-"))

            # COLUMN SERIAL
            _column = 10
            self.table_widget.setItem(i, _column, QTableWidgetItem(f"{node_table_row.serial_number}"))

            # COLUMN STATUS
            _column = 11
            self.table_widget.setItem(i, _column, QTableWidgetItem(node_table_row.get_status()))

            # COLUMN TESTING MODE
            _column = 12
            self.table_widget.setItem(i, _column, QTableWidgetItem(node_table_row.get_test_mode_description()))
            i += 1

            # start automatically node if just added
            if key in self._start_node_id:
                self.start_node(node_table_row)
                self._start_node_id.remove(key)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def on_context_menu(self, pos):
        index = self.table_widget.indexAt(pos)

        if not index.isValid():
            return

        sn_active = self.settings.value("sn_mnt_active", True, type=bool)
        row = index.row()

        key = self.table_widget.item(row, 0).text()  # Column 0 have unique key for channel/node_id

        node_table_row = self.table_rows[key]

        menu = QMenu()

        reset_action = menu.addAction("Reset device")
        info_action = menu.addAction("Info")
        add_info_action = menu.addAction("Add additional information")

        if sn_active:
            add_serial_action = menu.addAction("Add serial number")

        action = menu.exec_(self.table_widget.mapToGlobal(pos))

        # reset command from context menu
        if action == reset_action:
            self.reset_node(node_table_row)
            logger.debug(f'Reset Node ID: {node_table_row.node_id} by user')
            self._redraw_table = True

        # add additional information to context menu
        if action == add_info_action:
            dialog = AddInfoDialog(customer=node_table_row.customer, comment=node_table_row.comment)
            node_table_row.customer = dialog.customer
            node_table_row.comment = dialog.comment

        # add serial number action to context menu
        if sn_active:
            if action == add_serial_action:
                dialog = AddSNDialog(
                    channel=node_table_row.channel,
                    node_id=node_table_row.node_id,
                    serial_number=node_table_row.serial_number
                )
                node_table_row.serial_number = dialog.serial_number

        # node info command from context menu
        if action == info_action:
            logger.debug(f'Info for Node {node_table_row.node_id} on channel {node_table_row.channel}')
            # Create QMessageBox-Dialog

            text = ""

            try:
                text += f"Node ID: {node_table_row.node_id}\n"
            except:
                text += f"Node ID: -\n"

            try:
                text += f"Channel: {node_table_row.channel}\n"
            except:
                text += f"Channel: -\n"
            try:
                text += f"Manufacturer Device Name: {node_table_row.get_manufacturer_device_name()}\n"
            except:
                text += f"Manufacturer Device Name: -\n"
            try:
                text += f"Manufacturer Hardware Version: {node_table_row.get_manufacturer_hardware_version()}\n"
            except:
                text += f"Manufacturer Hardware Version: -\n"
            try:
                text += f"Manufacturer Software Version: {node_table_row.get_manufacturer_software_version()}\n"
            except:
                text += f"Manufacturer Software Version: -\n"
            try:
                text += f"CW/CCW movements: {str(node_table_row.get_cw_movements())}/{str(node_table_row.get_ccw_movements())}\n"
            except:
                text += f"CW/CCW movements: -/-\n"
            try:
                text += f"Accumulative operating time: {str(node_table_row.get_accumulative_operating_time())}\n"
            except:
                text += f"Accumulative operating time: -\n"
            try:
                text += f"Device temperature: {str(node_table_row.get_device_temp())} (max: {str(node_table_row.get_max_device_temp())})\n"
            except:
                text += f"Device temperature: - (max: -)\n"
            try:
                text += f"State: {str(node_table_row.node.state)}\n"
            except:
                text += f"State: -\n"
            try:
                text += f"Actual position: {str(node_table_row.get_actual_position())}\n"
            except:
                text += f"Actual position: -\n"
            try:
                text += f"Target position: {str(node_table_row.get_target_position())}\n"
            except:
                text += f"Target position: -\n"
            try:
                text += f"Control Word: {hex(node_table_row.get_control_word())}\n"
            except:
                text += f"Control Word: -\n"
            try:
                text += f"Status Word: {hex(node_table_row.get_status_word())}\n"
            except:
                text += f"Status Word: -\n"
            try:
                text += f"Actual current: {str(node_table_row.get_actual_current())}\n"
            except:
                text += f"Actual current: -\n"
            try:
                text += f"Rated/Max current: {str(node_table_row.get_rated_current())}/{str(node_table_row.get_max_current())}\n"
            except:
                text += f"Rated/Max current: -/-\n"
            try:
                text += f"Battery voltage: {hex(node_table_row.get_dc_link_circuit_voltage())}\n"
            except:
                text += f"Battery voltage: -\n"

            msg_box = QMessageBox()
            msg_box.setText(text)
            msg_box.setWindowTitle(f'Info Node {node_table_row.node_id}')
            msg_box.setStandardButtons(QMessageBox.Ok)

            result = msg_box.exec_()

    def refresh(self):
        for channel, network in enumerate(self.networks):
            try:
                if network is not None:
                    network.scanner.reset()
                    network.scanner.search()
                    time.sleep(0.05)

                    for node_id in network.scanner.nodes:
                        # check if node already in list otherwise add it
                        if node_id not in network:
                            self.add_node(network, node_id)
                            self._start_node_id.append(f'{channel}_{node_id}')

            except Exception as e:
                pass
                # logger.error(f"Error during node refresh: {e}")
                # logger.error(network.scanner.nodes)

        self._redraw_table = True

    @property
    def report_manager(self):
        return self._report_manager
