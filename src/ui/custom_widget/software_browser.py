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
        self.widget_main.setStyleSheet("background-color: transparent;")
        self.grid_main = QGridLayout(self.widget_main)
        self.grid_main.setContentsMargins(15, 15, 15, 15)
        self.grid_main.setSpacing(20)
        self.setAcceptDrops(True)

    def _get_software_column(self):
        width = self.size().width()
        self.column = width // (self.software_size + self.grid_main.spacing())
        if self.column == 0:
            self.column = 1

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.init_software()

        # self.setWidget(self.widget_main)

    def init_software(self):
        self._get_software_column()
        for i in reversed(range(self.grid_main.count())):
            widget = self.grid_main.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        column = 0
        row = 0
        for index, software in enumerate(self.software_list, 1):
            self._add_software_widget(software, row, column)
            column += 1
            if index % self.column == 0:
                row += 1
                column = 0
        self.widget_main.adjustSize()
        self.grid_main.update()
        self.setWidget(self.widget_main)

    def resize(self):
        self.widget_main.adjustSize()
        self.grid_main.update()

    def _add_software_widget(self, software, row, column):
        software_widget = SoftwareWidget(software, parent=self)
        software_widget.setFixedWidth(self.software_size)
        software_widget.setFixedHeight(self.software_size)
        self.grid_main.addWidget(software_widget, row, column)

    def dragEnterEvent(self, event):
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        mime_data: QMimeData = event.mimeData()
        urls = mime_data.urls()
        for url in urls:  # type: QUrl
            self.add_software_widget(url.path())
