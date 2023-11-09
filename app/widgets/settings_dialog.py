import logging
import cups

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog

from app.widgets.ui_settings_diag import Ui_SettingsDialog

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """
    Settings Dialog
    """
    def __init__(self):
        super().__init__()

        printers = None

        # load UI
        self._ui = Ui_SettingsDialog()
        self._ui.setupUi(self)

        # try to connect to CUPS
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
        except Exception as e:
            logger.debug(f"Exception during connecting CUPS: {e}")

        self.settings = QSettings("EMEC", "Tester")  # init QSettings
        printer = self.settings.value("printer", "None")  # get printer selection von settings file

        # if CUPS connected display all printers in list
        if printers is not None:
            for printer in printers:
                self._ui.cb_select_printer.addItem(printer)
        else:
            # otherwise add None to list
            self._ui.cb_select_printer.addItem("None")

        # if the saved printer is in list select it
        if printer in [self._ui.cb_select_printer.itemText(i) for i in range(self._ui.cb_select_printer.count())]:
            self._ui.cb_select_printer.setCurrentText(printer)
        else:
            self._ui.cb_select_printer.setCurrentText("None")
            logger.debug(f"Printer: <{self._printer}> not found in printer list")

        self._ui.sb_print_autom_timer.setValue(int(self.settings.value("label_print_timer", 60)))
        self._ui.cb_sn_active.setChecked(self.settings.value("sn_mnt_active", True, type=bool))
        self._ui.cb_printer_active.setChecked(self.settings.value("printer_active", True, type=bool))

        # label layout settings
        self._ui.sb_label_columns.setValue(self.settings.value("label_paper_columns", 2, type=int))
        self._ui.sb_column_width.setValue(self.settings.value("label_column_width", 60, type=int))
        self._ui.sb_column_height.setValue(self.settings.value("label_column_height", 30, type=int))

        # label padding
        self._ui.sb_padding_top.setValue(self.settings.value("label_column_top", 8, type=int))
        self._ui.sb_padding_bottom.setValue(self.settings.value("label_column_bottom", 8, type=int))
        self._ui.sb_padding_left.setValue(self.settings.value("label_column_left", 10, type=int))
        self._ui.sb_padding_right.setValue(self.settings.value("label_column_right", 10, type=int))

        # if exit with OK
        if self.exec_() == QDialog.Accepted:
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

