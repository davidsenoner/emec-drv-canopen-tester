import os
import logging
import datetime

from PySide6.QtCore import QDir
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QFileDialog, QWidget


class LogHandler(logging.Handler):
    def __init__(self, ui):
        super().__init__()

        # MAKE GLOBAL THE WIDGETS FROM MAIN WINDOW
        self._ui = ui

        # INIT HANDLER
        self.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.setLevel(logging.DEBUG)

        # CONNECT SIGNALS
        self._ui.btn_save_log.clicked.connect(self.save_log)

    def emit(self, record):
        self._ui.tedt_output_text.append(self.format(record))
        self._ui.tedt_output_text.moveCursor(QTextCursor.End)
        self._ui.tedt_output_text.ensureCursorVisible()

    # SAVE LOG FROM OUTPUT PANEL
    # ///////////////////////////////////////////////////////////////
    def save_log(self):
        # select a Path where to save Log
        temp = QFileDialog.getExistingDirectory(QWidget(), "Open Directory", QDir.homePath())
        if temp:
            date_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # get actual time
            filename = f'output_{date_time}.log'
            log_file = os.path.normpath(os.path.join(temp, filename))  # join path and filename

            with open(log_file, "w") as f:
                f.write(self._ui.tedt_output_text.toPlainText())  # save text from QTextEdit
