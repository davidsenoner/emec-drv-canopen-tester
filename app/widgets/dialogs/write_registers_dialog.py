import sys
from PyQt5.QtWidgets import QDialog

from app.widgets.ui_add_sn_diag import Ui_AddSNDialog
from app.modules.drives.emec_canopen import TITAN40_EMECDRV5_SLEWING_NODE_ID, TITAN40_EMECDRV5_LIFT_NODE_ID, IO_DRIVE_SLEWING_ID


class WriteRegistersDialog(QDialog):
    def __init__(self, node_id: int, channel: int = 0, **kwargs):
        """
        Open Dialog with input fields for serial number, hardware and firmware version
        :param node_id: Node ID of the selected drive
        :param channel: CANOpen channel
        :param kwargs: serial_number, hw_version, fw_version
        """
        super().__init__()

        self._serial_number = kwargs.get("serial_number", 0)
        self._hw_version = kwargs.get("hw_version", 0)
        self._fw_version = kwargs.get("fw_version", 0)

        self._ui = Ui_AddSNDialog()
        self._ui.setupUi(self)

        if self._serial_number == 0:
            self._ui.led_serial_number.clear()
        else:
            self._ui.led_serial_number.setText(str(self._serial_number))

        if self._hw_version == 0:
            self._ui.led_hw_version.clear()
        else:
            self._ui.led_hw_version.setText(str(self._hw_version))

        if self._fw_version == 0:
            self._ui.led_fw_version.clear()
        else:
            self._ui.led_fw_version.setText(str(self._sw_version))

        # Set lift node info to dialog
        if node_id == TITAN40_EMECDRV5_LIFT_NODE_ID:
            self._ui.lbl_drive_id.setText(f"<b>Lift</b> with Node ID: {node_id} on Channel: {channel}")

        # Set slewing node info to dialog
        elif node_id == TITAN40_EMECDRV5_SLEWING_NODE_ID:
            self._ui.lbl_drive_id.setText(f"<b>Slewing</b> with Node ID: {node_id} on Channel: {channel}")

        elif node_id == IO_DRIVE_SLEWING_ID:
            self._ui.lbl_drive_id.setText(f"<b>Slewing</b> with IO controlled signals")

        if self.exec_() == QDialog.Accepted:
            check_sn = self._ui.led_serial_number.text()
            if check_sn.isdigit():
                self._serial_number = int(check_sn)
            else:
                self._serial_number = 0

    def get_serial_number(self) -> int:
        return self._serial_number

    def get_hw_version(self):
        return self._hw_version

    def get_fw_version(self):
        return self._fw_version
