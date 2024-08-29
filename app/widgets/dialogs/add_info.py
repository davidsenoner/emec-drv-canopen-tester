import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

from app.widgets.ui_add_info_diag import Ui_AddInfoDialog


class AddInfoDialog(QDialog):
    def __init__(self,
                 customer: str = "",
                 comment: str = ""
                 ):
        super().__init__()

        self._customer = customer
        self._comment = comment

        self._ui = Ui_AddInfoDialog()
        self._ui.setupUi(self)

        self._ui.led_customer.setText(self.customer)
        self._ui.txt_comment.setText(self.comment)

        if self.exec_() == QDialog.Accepted:
            self.customer = self._ui.led_customer.text()
            self.comment = self._ui.txt_comment.toPlainText()

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
