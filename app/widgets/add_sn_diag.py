import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

from app.widgets.ui_add_sn_diag import Ui_AddSNDialog


class AddSNDialog(QDialog):
    def __init__(self,
                 serial_number: int = 0
                 ):
        super().__init__()

        self._serial_number = serial_number

        self._ui = Ui_AddSNDialog()


        self._ui.setupUi(self)

        if self.serial_number == 0:
            sn_init = ""
        else:
            sn_init = str(self.serial_number)

        self._ui.led_serial_number.setText(sn_init)

        if self.exec_() == QDialog.Accepted:
            self.serial_number = int(self._ui.led_serial_number.text())

    @property
    def serial_number(self) -> int:
        return self._serial_number

    @serial_number.setter
    def serial_number(self, sn: int) -> None:
        self._serial_number = sn
