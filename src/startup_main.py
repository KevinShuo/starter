from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import *
from src.views.startup_view import StartupViewer
import sys

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    w = StartupViewer()
    sys.exit(app.exec())
