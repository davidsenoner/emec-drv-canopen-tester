import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

from app.widgets.ui_add_sn_diag import Ui_AddSNDialog
from app.modules.drives.emec_canopen import TITAN40_EMECDRV5_SLEWING_NODE_ID, TITAN40_EMECDRV5_LIFT_NODE_ID


class AddSNDialog(QDialog):
    def __init__(self,
                 node_id: int,
                 channel: int,
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

        # Set lift node info to dialog
        if node_id == TITAN40_EMECDRV5_LIFT_NODE_ID:
            self._ui.lbl_drive_id.setText(f"<b>Lift</b> with Node ID: {node_id} on Channel: {channel}")

        # Set slewing node info to dialog
        elif node_id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            self._ui.lbl_drive_id.setText(f"<b>Slewing</b> with Node ID: {node_id} on Channel: {channel}")

        if self.exec_() == QDialog.Accepted:
            check_sn = self._ui.led_serial_number.text()
            if check_sn.isdigit():
                self.serial_number = int(check_sn)
            else:
                self.serial_number = 0

    @property
    def serial_number(self) -> int:
        return self._serial_number

    @serial_number.setter
    def serial_number(self, sn: int) -> None:
        self._serial_number = sn
