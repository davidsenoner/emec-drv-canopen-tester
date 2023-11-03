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
        self._printer = self.settings.value("printer", "None")  # get printer selection von settings file

        # if CUPS connected display all printers in list
        if printers is not None:
            for printer in printers:
                self._ui.cb_select_printer.addItem(printer)
        else:
            # otherwise add None to list
            self._ui.cb_select_printer.addItem("None")

        items = [self._ui.cb_select_printer.itemText(i) for i in range(self._ui.cb_select_printer.count())]

        # if the saved printer is in list select it
        if self._printer in items:
            self._ui.cb_select_printer.setCurrentText(self._printer)
        else:
            self._ui.cb_select_printer.setCurrentText("None")
            logger.debug(f"Printer: <{self._printer}> not found in printer list")

        if self.exec_() == QDialog.Accepted:
            # save selected  printer to QSettings file
            self.settings.setValue("printer", self._ui.cb_select_printer.currentText())
