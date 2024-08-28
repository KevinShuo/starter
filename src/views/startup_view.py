# -*- coding: utf-8 -*-
import functools
import getpass
import dataclasses
import json
import os
from enum import Enum
from typing import List, Optional

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ..models.startup.software_dataclass import SoftwareData
from ..ui.startup_ui import StartupUI
from ..ui.custom_widget.software_browser import SoftwareBrowser
from ..models.startup.startup_db import StartupDB
from ..config import *
from ..util import *


class DBType(Enum):
    local = 0
    server = 1


class StartupViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_project = None
        self.db_startup = None
        # global config
        self.window_size = (785, 649)
        # title
        self.window_title = "软件启动器"
        self.startup_ui = StartupUI()
        # pieces of software list
        self.software_list: List[SoftwareData] = []
        # 显示
        self.startup_ui.setupUi(self)
        self.init_ui()
        # 样式初始化
        self.init_style()
        # 数据库操作
        self.init_db()
        # 初始化tab
        self.init_tab()

    def init_ui(self):
        self.cache = self._get_save_size()
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../resources", "logo.ico")))
        self.setIconSize(QSize(128, 128))
        if self.cache:
            self.resize(self.cache.width, self.cache.height)
            self.move(self.cache.x, self.cache.y)
        else:
            self.resize(*self.window_size)
            # move bottom left
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()

            window_grometry = self.frameGeometry()
            x = screen_geometry.x() + screen_geometry.width() - window_grometry.width()
            y = screen_geometry.y() + screen_geometry.height() - window_grometry.height()
            self.move(x, y)
        # menu
        self.init_project_menu()

        self.show()

    def init_project_menu(self):
        menu_projects = self.startup_ui.menuBar.addMenu("Projects")
        self.db_startup = StartupDB(self.db_server_path)
        tables = self.db_startup.get_all_tables()
        for table in tables:
            action_project = menu_projects.addAction('_'.join(str(table).split("_")))
            action_project.triggered.connect(functools.partial(self.clicked_project_action, table))

    def clicked_project_action(self, menu_name: str):
        self.write_config(menu_name)
        self.init_db()
        self.startup_ui.tabWidget.clear()
        self.init_tab()

    def init_db(self):
        config_data = self.load_config()
        current_workspace = config_data["current_workspace"]
        # 初始化
        if config_data["current_type"] == DBType.server.name:
            self.db_startup = StartupDB(self.db_server_path)
            if not current_workspace:
                workspace = self.db_startup.initialize()
                self.current_project = workspace
                self.setWindowTitle(f"[ {current_workspace} ] {self.window_title}")
            else:
                self.db_startup.initialize(current_workspace)
                self.current_project = current_workspace
                self.setWindowTitle(f"[ {current_workspace} ] {self.window_title}")
        self.software_list = self.db_startup.get_software()

    def init_style(self):
        with open(os.path.join(os.path.dirname(__file__), "../ui/qss/startup.css"), "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())

    def init_tab(self):
        for index, tab_name in enumerate(self.software_tabs):
            self.add_tab(tab_name)
        if self.cache:
            for c in range(self.startup_ui.tabWidget.count()):
                tab_title = self.startup_ui.tabWidget.tabText(c)
                if tab_title == self.cache.current_tab:
                    self.startup_ui.tabWidget.setCurrentIndex(c)

    def add_tab(self, name: str):
        """
            添加tab
        """
        widget_tab = QWidget()
        vbox_tab_main = QVBoxLayout(widget_tab)
        vbox_tab_main.setContentsMargins(0, 0, 0, 0)
        all_software = tuple([i for i in self.software_list if i.tab == name])
        self.scroll_main = SoftwareBrowser(all_software)
        vbox_tab_main.addWidget(self.scroll_main)
        self.startup_ui.tabWidget.addTab(widget_tab, name)

    def _get_software_browser(self, tab_index: int) -> SoftwareBrowser:
        widget = self.startup_ui.tabWidget.widget(tab_index)
        return [i for i in widget.findChildren(SoftwareBrowser)][0]

    @property
    def db_local_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "../../db/local.db")

    @property
    def db_server_path(self) -> Optional[str]:
        server_path = os.path.join(os.path.dirname(__file__), "../config/server_startup_db.txt").replace('\\', '/')
        if not os.path.exists(server_path):
            return
        with open(server_path, "r",
                  encoding="utf-8") as file:
            return file.read()

    @property
    def software_tabs(self) -> list:
        # if not self.software_list:
        #     raise AttributeError("Must get softwares data")
        return sorted(list(set([i.tab for i in self.software_list])))

    @staticmethod
    def load_config() -> dict:
        startup_path = os.path.join(os.path.dirname(__file__), "../config/startup.json").replace('\\', '/')

        def write_config():
            with open(startup_path, "w", encoding="utf-8") as file_write:
                d = {"current_workspace": "software", "current_type": DBType.server.name}
                json.dump(d, file_write)
                return d

        if not os.path.exists(startup_path):
            return write_config()
        else:
            with open(startup_path, "r+", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    return data
                except:
                    return write_config()

    def write_config(self, workspace: str):
        """
            写startup config配置
        Args:
            workspace:

        Returns:

        """
        with open(os.path.join(os.path.dirname(__file__), "../config/startup.json"), "w+") as file:
            d = {"current_workspace": workspace, "current_type": DBType.server.name}
            json.dump(d, file)
            return d

    def __del__(self):
        try:
            self.db_startup.close()
        except:
            pass

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self._set_window_size(self.x(), self.y(), self.width(), self.height())

    def resizeEvent(self, event):
        # print(event.size())
        super().resizeEvent(event)
        tab_bar = self.startup_ui.tabWidget.tabBar()
        if event.size().width() < 200:
            tab_bar.hide()
        else:
            tab_bar.show()

    @staticmethod
    def _get_save_size():
        @dataclasses.dataclass
        class WindowSize:
            x: int
            y: int
            width: int
            height: int
            current_tab: str
            current_project: str

        startup_path = get_startup_path()
        json_path = os.path.join(startup_path, "config.json")
        if os.path.exists(json_path):
            with open(os.path.join(startup_path, "config.json"), "r", encoding="utf-8") as file:
                data = json.load(file)
                return WindowSize(**data)

    def _set_window_size(self, x: int, y: int, width: int, height: int):
        startup_path = get_startup_path()
        with open(os.path.join(startup_path, "config.json"), "w", encoding="utf-8") as file:
            size = {"x": x, "y": y, "width": width, "height": height,
                    "current_tab": self.startup_ui.tabWidget.tabText(self.startup_ui.tabWidget.currentIndex()),
                    "current_project": self.current_project}
            file.write(json.dumps(size))
