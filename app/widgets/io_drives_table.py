import logging
import time
import platform
from canopen import Network, BaseNode402

from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHeaderView, QTableWidget, QMenu, QMessageBox
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject, QTimer, QSettings
from PyQt5.QtGui import QCursor, QColor, QBrush

from app.modules.io.remoteio import MoxaE1242
from app.modules.drives.emec_l2_l3 import EMECL2L3Drive, EmecL2L3IO
from app.modules.test_report import Label, TestReportManager
from app.modules.drives.defines import IO_DRIVE_SLEWING_ID

logger = logging.getLogger(__name__)


class IODrivesTable(QObject):
    def __init__(self, widget: QTableWidget, remote_io: MoxaE1242):
        super().__init__()

        self.table_widget = widget
        self.remote_io = remote_io
        self._headers = ["Type", "Start", "Stop", "CW", "CCW", "Position", "Duration", "Serial Number", "State"]

        self.table_widget.setColumnCount(len(self._headers))
        self.table_widget.setHorizontalHeaderLabels(self._headers)
        self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.table_widget.customContextMenuRequested.connect(self.on_context_menu)
        self.table_widget.horizontalHeader().setContentsMargins(10, 0, 10, 0)

        self.refresh_table_timer = QTimer()
        self.refresh_table_timer.start(1000)
        self.refresh_table_timer.timeout.connect(self.draw_table)

        self.settings = QSettings("EMEC", "Tester")
        params_drive0 = {
            "remote_io": self.remote_io,
            "enable_pin": self.settings.value("io_drive_0_enable_pin", 0, type=int),
            "direction_pin": self.settings.value("io_drive_0_direction_pin", 1, type=int),
            "angle_pin": self.settings.value("io_drive_0_angle_pin", 0, type=int),
            "voltage_at_min_angle": self.settings.value("AI0_voltage_0deg", 0.5, type=float),
            "voltage_at_max_angle": self.settings.value("AI0_voltage_359deg", 4.5, type=float),
            "en_active_high": self.settings.value("EN0_active_high", True, type=bool),
            "dir_active_high": self.settings.value("DIR0_active_high", True, type=bool)
        }

        params_drive1 = {
            "remote_io": self.remote_io,
            "enable_pin": self.settings.value("io_drive_1_enable_pin", 2, type=int),
            "direction_pin": self.settings.value("io_drive_1_direction_pin", 3, type=int),
            "angle_pin": self.settings.value("io_drive_1_angle_pin", 1, type=int),
            "voltage_at_min_angle": self.settings.value("AI1_voltage_0deg", 0.5, type=float),
            "voltage_at_max_angle": self.settings.value("AI1_voltage_359deg", 4.5, type=float),
            "en_active_high": self.settings.value("EN1_active_high", True, type=bool),
            "dir_active_high": self.settings.value("DIR1_active_high", True, type=bool)
        }

        self.drive_0 = EMECL2L3Drive(EmecL2L3IO(**params_drive0))
        self.drive_1 = EMECL2L3Drive(EmecL2L3IO(**params_drive1))

        # create by default a table with 2 rows
        self.table_rows = {0: self.drive_0, 1: self.drive_1}

        for _ in self.table_rows.keys():
            i = self.table_widget.rowCount()
            self.table_widget.insertRow(i)
            self.table_widget.setRowHeight(i, 40)

        self.draw_table()

    def set_report_manager(self, report_manager: TestReportManager):
        self.drive_1.on_label_ready.connect(report_manager.add_label)
        self.drive_0.on_label_ready.connect(report_manager.add_label)
        self.drive_0.on_print_label.connect(report_manager.print_label_from_serial_number)
        self.drive_1.on_print_label.connect(report_manager.print_label_from_serial_number)

    def draw_table(self):

        for i, remote_io_table_row in self.table_rows.items():

            column = 0
            self.table_widget.setItem(i, column, QTableWidgetItem(str(remote_io_table_row)))

            # COLUMN START BUTTON
            column = 1
            btn_start = QPushButton('Start')
            btn_start.setMaximumSize(QSize(60, 35))
            btn_start.setCursor(QCursor(Qt.PointingHandCursor))
            btn_start.clicked.connect(
                lambda arg, n=remote_io_table_row: self.start_node(n)
            )
            self.table_widget.setCellWidget(i, column, btn_start)

            # COLUMN STOP BUTTON
            column = 2
            btn_stop = QPushButton('Stop')
            btn_stop.setMaximumSize(QSize(60, 35))
            btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
            btn_stop.clicked.connect(
                lambda arg, n=remote_io_table_row: self.stop_node(n)
            )
            self.table_widget.setCellWidget(i, column, btn_stop)

            # COLUMN CW MOVEMENTS
            column = 3
            self.table_widget.setItem(i, column, QTableWidgetItem(str(remote_io_table_row.get_cw_movements())))

            # COLUMN CCW MOVEMENTS
            column = 4
            self.table_widget.setItem(i, column, QTableWidgetItem(str(remote_io_table_row.get_ccw_movements())))

            # COLUMN ACTUAL ANGLE
            column = 5
            self.table_widget.setItem(i, column, QTableWidgetItem(f"{round(remote_io_table_row.get_actual_angle())}°"))

            # COLUMN DURATION
            column = 6
            seconds = remote_io_table_row.get_elapsed_time()
            duration = str(seconds // 60) + "m " + str(seconds % 60) + "s"
            self.table_widget.setItem(i, column, QTableWidgetItem(duration))

            # COLUMN SERIAL
            column = 7
            self.table_widget.setItem(i, column, QTableWidgetItem(f"{remote_io_table_row.serial_number}"))

            # COLUMN STATUS
            column = 8
            self.table_widget.setItem(i, column, QTableWidgetItem(remote_io_table_row.get_status()))

            # COLUMN TESTING MODE
            column = 9
            #self.table_widget.setItem(i, column, QTableWidgetItem(remote_io_table_row.get_test_mode_description()))

            i += 1  # IMPORTANT: increment row counter only once!!!

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)


    @staticmethod
    def start_node(row: EMECL2L3Drive):
        try:
            row.start_test()
        except Exception as e:
            logger.debug(f'Error during start test command: {e}')
            return

    @staticmethod
    def stop_node(row: EMECL2L3Drive):
        try:
            row.stop_test("Stopped by user")
        except Exception as e:
            logger.debug(f'Error during stop test command: {e}')