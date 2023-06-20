import sys

from PyQt5.QtWidgets import QApplication
from app.widgets.main import MainWindow

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)

        app.setOrganizationName('EMEC')
        app.setApplicationName('EMEC Drive End-Of-Line Tester')
        app.setApplicationVersion('1.4')

        w = MainWindow()
        sys.exit(app.exec())
    else:
        print("QApplication instance already running")
