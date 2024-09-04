from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ..custom_widget.software_widget import SoftwareWidget
from ...util import log_caller


class SoftwareBrowser(QScrollArea):
    def __init__(self, software_list: list, parent=None):
        super().__init__(parent)
        self.software_list = software_list
        self.software_size = 120
        self.widget_main = QWidget()
        self.widget_main.resize(self.size())
        self.widget_main.setStyleSheet("background-color: transparent;")
        self.grid_main = QGridLayout(self.widget_main)
        # self.grid_main.setContentsMargins(15, 15, 15, 15)
        self.grid_main.setSpacing(10)
        # self.setAcceptDrops(True)
