import sys

from PyQt5.QtWidgets import QApplication
from app.widgets.main import MainWindow

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)

        app.setOrganizationName('EMEC')
        app.setApplicationName('EMEC Drive EOL Test')

        w = MainWindow()
        sys.exit(app.exec())
    else:
        print("QApplication instance already running")
