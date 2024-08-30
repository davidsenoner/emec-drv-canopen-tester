import sys
from PyQt5.QtWidgets import QApplication
from app import MainWindow

VERSION = "2.8.1"  # Version number

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            print(f"{sys._MEIPASS =}")

        app.setOrganizationName('EMEC')
        app.setApplicationName('EMEC Drive End-Of-Line Tester')
        app.setApplicationVersion(VERSION)

        w = MainWindow(VERSION)

        sys.exit(app.exec())
    else:
        print("QApplication instance already running")
