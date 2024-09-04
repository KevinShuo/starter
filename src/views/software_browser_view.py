from os import close

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ..ui.custom_widget.software_browser import SoftwareBrowser
from ..views.software_view import SoftwareView


class SoftwareBrowserView(SoftwareBrowser):
    def __init__(self, software_list: list, parent=None):
        super().__init__(software_list, parent)
        # self.setWidgetResizable(True)  # 确保窗口大小改变时，内容可以重新调整大小

    def _get_software_column(self):
        width = self.size().width()
        column = width // (self.software_size + 10)
        if column == 0:
            return 1
        return column

    def resizeEvent(self, event):
        if self.grid_main.columnCount() != self._get_software_column():
            self.init_software()
            self.widget_main.adjustSize()
            # self.grid_main.update()
            self.setWidget(self.widget_main)
        super().resizeEvent(event)

        # self.setWidget(self.widget_main)

    def init_software(self):
        column_count = self._get_software_column()
        for i in reversed(range(self.grid_main.count())):
            widget = self.grid_main.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        column = 0
        row = 0
        for index, software in enumerate(self.software_list, 1):
            self._add_software_widget(software, row, column)
            column += 1
            if index % column_count == 0:
                row += 1
                column = 0

    def _add_software_widget(self, software, row, column):
        software_widget = SoftwareView(software, parent=self)
        software_widget.setMinimumWidth(self.software_size)
        software_widget.setMaximumHeight(self.software_size)
        self.grid_main.addWidget(software_widget, row, column,Qt.AlignCenter)
        self.widget_main.adjustSize()
        self.grid_main.update()
