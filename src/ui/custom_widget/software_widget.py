# -*- coding: utf-8 -*-
import os
import subprocess
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from src.models.startup.software_dataclass import SoftwareData
from .auto_dismiss_message import AutoDismissMessage


class SoftwareWidget(QFrame):
    def __init__(self, software_data: SoftwareData, parent=None):
        super().__init__(parent)
        self.original_geometry = None
        self.pic_size = 50
        self.software_data = software_data
        self.setupUI()
        self.add_shadow()
        self.init_style()

        self.animation = QPropertyAnimation(self, b"geometry")
        self.scale_factor = 5

    def init_style(self):
        with open(os.path.join(os.path.dirname(__file__), "../qss/software_widget.css"), "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(2, 2)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow)

    def add_label_shadow(self, label: QLabel):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(3, 3)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 180))
        label.setGraphicsEffect(shadow)

    def setupUI(self):
        self.setObjectName("SoftwareWidget")
        vbox_main = QVBoxLayout(self)
        # self.setMinimumSize(0, 0)
        self.label_picture = QLabel()
        self.label_picture.setObjectName("label_picture")
        pix = QPixmap(self.software_data.ico).scaledToWidth(self.pic_size)
        self.label_picture.setPixmap(pix)
        self.add_label_shadow(self.label_picture)
        self.label_name = QLabel(self.software_data.name)
        self.label_name.setObjectName("label_name")
        vbox_main.addWidget(self.label_picture, 1, Qt.AlignmentFlag.AlignCenter)
        vbox_main.addWidget(self.label_name, 1, Qt.AlignmentFlag.AlignCenter)
        self.setToolTip(self.software_data.description if self.software_data.description else self.software_data.name)


