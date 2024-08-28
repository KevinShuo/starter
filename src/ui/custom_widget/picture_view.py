# -*- coding: utf-8 -*-
# @Time : 2024/8/13 14:36
# @Author : Mr.wang
# @Email : 204062518@qq.com
# @File : picture_view.py
# @Project : Viewer
from PySide2.QtGui import QPainter, QFont, QColor, QWheelEvent, QPixmap
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *


class PictureView(QLabel):
    def __init__(self, parent=None):
        super(PictureView, self).__init__(parent)
        self.text = "Picture View"
        self.setStyleSheet("border: 1px dashed black;")
        self.factory = 1.2

    def paintEvent(self, arg__1):
        super(PictureView, self).paintEvent(arg__1)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setFont(QFont("Arial Black", 30, QFont.Bold))
        painter.setPen(QColor(200, 200, 200, 100))

        rect = self.rect()
        text_rect = painter.boundingRect(rect, Qt.AlignCenter, self.text)
        text_rect.moveCenter(rect.center())

        painter.drawText(text_rect, Qt.AlignCenter, self.text)
        painter.end()

    def wheelEvent(self, event: QWheelEvent):
        super(PictureView, self).wheelEvent(event)
        pixmap: QPixmap = self.pixmap()
        if not pixmap:
            return
        rect = pixmap.size()
        width, height = rect.width(), rect.height()
        if event.angleDelta().y() > 0:
            new_w = width * self.factory
            new_pix = pixmap.scaledToWidth(new_w, Qt.SmoothTransformation)
            self.setPixmap(new_pix)
        else:
            new_w = width * (1 / self.factory)
            new_pix = pixmap.scaledToWidth(new_w, Qt.SmoothTransformation)
            self.setPixmap(new_pix)
