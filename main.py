import sys
from PyQt5.QtWidgets import QApplication
from app import MainWindow

VERSION = "2.2.2"  # Version number

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)

        app.setOrganizationName('EMEC')
        app.setApplicationName('EMEC Drive End-Of-Line Tester')
        app.setApplicationVersion(VERSION)

        w = MainWindow(VERSION)

        sys.exit(app.exec())
    else:
        print("QApplication instance already running")
