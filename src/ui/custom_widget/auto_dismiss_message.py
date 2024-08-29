# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enum import Enum


class MsgLevel(Enum):
    info = "info"
    warning = "warning"
    critical = "critical"


class AutoDismissMessage(QLabel):
    def __init__(self, parent=None, message="", msg_type: MsgLevel = MsgLevel.info, duration=3000):
        super().__init__(parent)

        self.setText(message)
        self.setAlignment(Qt.AlignCenter)
        # self.setFixedSize(250, 50)
        self.setStyleSheet(self.get_style(msg_type))
        self.move_to_top_center()
        self.start_fade_in()
        QTimer.singleShot(duration, self.start_fade_out)
        f = QFont('SimHei', 12)
        f.setBold(True)
        self.setFont(f)
        self.add_shadow()
        self.adjustSize()
        self.show()

    def add_shadow(self):
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(3, 3)
        effect.setBlurRadius(15)
        effect.setColor(QColor(0, 0, 0, 200))
        self.setGraphicsEffect(effect)

    def get_style(self, msg_type: MsgLevel):
        if msg_type.value == "info":
            return "background-color: #f7cac9; border: 1px solid #ccccc0;border-radius: 10px;"
        elif msg_type.value == "warning":
            return "background-color: yellow; border: 1px solid black;border-radius: 10px;"
        elif msg_type.value == "critical":
            return "background-color: red; border: 1px solid black; color: white;border-radius: 10px;"
        else:
            return "background-color: #f7cac9; border: 1px solid black;border-radius: 10px;"

    def move_to_top_center(self):
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = (parent_geometry.width() - self.width()) // 2
            y = 30
            self.move(x, y)

    def start_move(self):
        self.move_animation = QPropertyAnimation(self, b'geometry')
        self.move_animation.setDuration(500)
        self.move_animation.setStartValue(100)
        self.move_animation.setEndValue(30)
        self.move_animation.start()

    def start_fade_out(self):
        # 创建透明度效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(600)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(self.close)
        self.fade_animation.start()

    def start_fade_in(self):
        # 创建透明度效果
        self.opacity_effect_in = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect_in)
        self.fade_animation_in = QPropertyAnimation(self.opacity_effect_in, b"opacity")
        self.fade_animation_in.setDuration(600)
        self.fade_animation_in.setStartValue(0)
        self.fade_animation_in.setEndValue(1)
        self.fade_animation_in.start()
