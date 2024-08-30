from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ..ui.custom_widget.software_browser import SoftwareBrowser
from ..views.software_view import SoftwareView


class SoftwareBrowserView(SoftwareBrowser):
    def __init__(self, software_list: list, parent=None):
        super().__init__(software_list, parent)

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
        software_widget = SoftwareView(software, parent=self)
        software_widget.setMinimumWidth(self.software_size)
        software_widget.setMinimumHeight(self.software_size)
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
