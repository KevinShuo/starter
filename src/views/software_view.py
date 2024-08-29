import os
import subprocess
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ..models.startup.software_dataclass import SoftwareData
from ..ui.custom_widget.auto_dismiss_message import AutoDismissMessage, MsgLevel
from ..ui.custom_widget.software_widget import SoftwareWidget


class SoftwareView(SoftwareWidget):
    def __init__(self, software_data: SoftwareData, parent=None):
        super().__init__(software_data, parent)

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
            pass

    def install_software(self):
        """
            主动安装程序
        """
        if not self.software_data.install_program:
            AutoDismissMessage(message="当前应用未设置安装程序，请联系TD", msg_type=MsgLevel.critical,
                               parent=self.parent())
            return
        if not os.path.exists(self.software_data.install_program):
            AutoDismissMessage(message="安装程序路径不存在，请联系TD", msg_type=MsgLevel.critical,
                               parent=self.parent())
            return
        subprocess.run([self.software_data.install_program])
