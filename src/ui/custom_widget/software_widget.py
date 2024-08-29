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
        super().__init__()
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
        self.setMinimumSize(0, 0)
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

    def enterEvent(self, event):
        # 记录原始几何尺寸，只在初次记录一次
        if self.original_geometry is None:
            self.original_geometry = self.geometry()

        # 停止任何正在进行的动画
        self.animation.stop()

        # 鼠标进入时重置位置到原始几何尺寸
        self.setGeometry(self.original_geometry)

        # 设置动画开始和结束值
        self.animation.setStartValue(self.original_geometry)
        end_rect = QRect(self.original_geometry.x() - self.scale_factor, self.original_geometry.y() - self.scale_factor,
                         self.original_geometry.width() + self.scale_factor * 2,
                         self.original_geometry.height() + self.scale_factor * 2)
        self.animation.setEndValue(end_rect)
        self.animation.start()

    def leaveEvent(self, event):
        # 停止任何正在进行的动画
        self.animation.stop()

        # 鼠标离开时重置位置到放大的几何尺寸
        end_rect = QRect(self.original_geometry.x() - self.scale_factor, self.original_geometry.y() - self.scale_factor,
                         self.original_geometry.width() + self.scale_factor * 2,
                         self.original_geometry.height() + self.scale_factor * 2)
        self.setGeometry(end_rect)

        # 设置动画开始和结束值
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.original_geometry)
        self.animation.start()

    def mouseDoubleClickEvent(self, *args, **kwargs):
        if not os.path.exists(self.software_data.path):
            QMessageBox.information(self, "提示", "检查到软件未安装，即将开始安装")
            self.install_software()
        try:
            subprocess.Popen([self.software_data.path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            message = AutoDismissMessage(message="启动成功", parent=self.parent())

        except:
            QMessageBox.critical(self, "错误", traceback.format_exc())

    def install_software(self):
        pass
