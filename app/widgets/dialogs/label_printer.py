import logging
import cups
import subprocess, platform
from pathlib import Path

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog

from app.widgets.ui_labelprinter_diag import Ui_LabelPrinterDialog
from app.modules.test_report import Label, TestReportManager, print_pdf

logger = logging.getLogger(__name__)


class LabelPrinterDialog(QDialog):
    """
    Settings Dialog
    """

    def __init__(self):
        super().__init__()

        printers = None

        # load UI
        self._ui = Ui_LabelPrinterDialog()
        self._ui.setupUi(self)
        self._label_temp_path = None

        # try to connect to CUPS
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
        except Exception as e:
            logger.error(f"Exception during connecting CUPS: {e}")

        self.settings = QSettings("EMEC", "Tester")  # init QSettings
        printer = self.settings.value("printer", "None")  # get printer selection von settings file
        self._ui.cb_select_printer.addItem("None")

        # if CUPS connected display all printers in list
        if printers is not None:
            for printer in printers:
                self._ui.cb_select_printer.addItem(printer)

        # if the saved printer is in list select it
        if printer in [self._ui.cb_select_printer.itemText(i) for i in range(self._ui.cb_select_printer.count())]:
            self._ui.cb_select_printer.setCurrentText(printer)
        else:
            self._ui.cb_select_printer.setCurrentText("None")
            logger.debug(f"Printer: <{printer}> not found in printer list")

        self._ui.sb_print_autom_timer.setValue(int(self.settings.value("label_print_timer", 60)))
        self._ui.cb_sn_active.setChecked(self.settings.value("sn_mnt_active", True, type=bool))
        self._ui.cb_printer_active.setChecked(self.settings.value("printer_active", True, type=bool))

        # label layout settings
        self._ui.sb_label_columns.setValue(self.settings.value("label_paper_columns", 1, type=int))
        self._ui.sb_column_width.setValue(self.settings.value("label_column_width", 60, type=int))
        self._ui.sb_column_height.setValue(self.settings.value("label_column_height", 40, type=int))

        # label padding
        self._ui.sb_padding_top.setValue(self.settings.value("label_column_top", 4, type=int))
        self._ui.sb_padding_bottom.setValue(self.settings.value("label_column_bottom", 4, type=int))
        self._ui.sb_padding_left.setValue(self.settings.value("label_column_left", 0, type=int))
        self._ui.sb_padding_right.setValue(self.settings.value("label_column_right", 0, type=int))
        self._ui.sb_label_file_cache.setValue(self.settings.value("label_files_cache", 50, type=int))

        self._ui.btn_print_test_label.clicked.connect(self.on_print_test_label)

        ret = self.exec_()

        # delete temporary label file when exit from settings dialog
        if self._label_temp_path is not None:
            self._label_temp_path.unlink(missing_ok=True)

        # if exit with OK
        if ret == QDialog.Accepted:
            self.settings.setValue("printer_active", self._ui.cb_printer_active.isChecked())
            self.settings.setValue("sn_mnt_active", self._ui.cb_sn_active.isChecked())
            self.settings.setValue("printer", self._ui.cb_select_printer.currentText())
            self.settings.setValue("label_print_timer", self._ui.sb_print_autom_timer.value())

            # label settings
            self.settings.setValue("label_paper_columns", self._ui.sb_label_columns.value())
            self.settings.setValue("label_column_width", self._ui.sb_column_width.value())
            self.settings.setValue("label_column_height", self._ui.sb_column_height.value())

            # label padding
            self.settings.setValue("label_column_top", self._ui.sb_padding_top.value())
            self.settings.setValue("label_column_bottom", self._ui.sb_padding_bottom.value())
            self.settings.setValue("label_column_left", self._ui.sb_padding_left.value())
            self.settings.setValue("label_column_right", self._ui.sb_padding_right.value())
            self.settings.setValue("label_files_cache", self._ui.sb_label_file_cache.value())

    def on_print_test_label(self) -> None:
        """
        Print a test-label with selected printer
        :return: None
        """
        path = self.generate_test_label()  # get path of generated test label to print
        printer = self._ui.cb_select_printer.currentText()  # get selected printer
        if path is not None:
            print_pdf(path=path, printer=printer)

    def on_open_test_label(self) -> None:
        """
        Open test-label PDF in PDF viewer without printing it
        :return: None
        """
        path = self.generate_test_label()  # get path of generated test label to print

        if path is not None:
            subprocess.Popen([path], shell=True)
            self._label_temp_path = Path(path)

    def generate_test_label(self) -> str:
        """
        Generate a test-label for layout design
        :return: str - path of label file used for printing or opening
        """

        report_manager = TestReportManager()

        i = 0
        while i < report_manager.columns_count:
            label = Label(20231120 + i)
            label.node_id = 13
            label.mean_current = 400
            label.cw_block_torque = 42
            label.ccw_block_torque = 40
            label.type = "SLEWING"
            report_manager.add_label(label)
            i += 1

        return report_manager.last_label_path
