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

from ..config.config import G_title, G_version
from ..models.effect_style import apply_blur_effect
from ..models.startup.software_dataclass import SoftwareData
from ..ui.startup_ui import StartupUI
from ..views.software_browser_view import SoftwareBrowserView
from ..models.startup.startup_db import StartupDB
from ..config import *
from ..util import *


class DBType(Enum):
    local = 0
    server = 1


class StartupViewer(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StartupViewer, cls).__new__(cls)
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            super().__init__()
            hwnd = int(self.winId())  # 获取窗口句柄
            apply_blur_effect(hwnd)
            self.current_project = None
            self.db_startup = None
            # global config
            self.window_size = (785, 649)
            # title
            self.window_title = f"{G_title}_v{G_version}"
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
            self._is_initialized = True

            # 设置应用程序图标
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "../resources", "logo.ico")))
            self.tray_icon.setToolTip("DCC启动器")

            # 创建托盘图标的菜单
            tray_menu = QMenu()

            restore_action = QAction("恢复", self)
            restore_action.triggered.connect(self.show)
            tray_menu.addAction(restore_action)

            exit_action = QAction("退出", self)
            exit_action.triggered.connect(QApplication.instance().quit)
            tray_menu.addAction(exit_action)

            self.tray_icon.setContextMenu(tray_menu)

            # 双击托盘图标恢复窗口
            self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def init_ui(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
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
        self.startup_ui.tabWidget.currentChanged.connect(self.switch_tab)
        self.show()

    def init_project_menu(self):
        menu_projects = self.startup_ui.menuBar.addMenu("Projects")
        self.db_startup = StartupDB(self.db_server_path)
        tables = self.db_startup.get_all_tables()
        for table in tables:
            action_project = menu_projects.addAction('_'.join(str(table).split("_")))
            action_project.triggered.connect(functools.partial(self.clicked_project_action, table))
        refresh = self.startup_ui.menuBar.addAction("Refresh")
        refresh.triggered.connect(functools.partial(self.clicked_refresh_action))

    def clicked_project_action(self, menu_name: str):
        self.write_config(menu_name)
        self.init_db()
        self.startup_ui.tabWidget.clear()
        self.init_tab()
        # self.scroll_main.resize()

    def clicked_refresh_action(self):
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

    def switch_tab(self, current_index: int):
        widget = self.startup_ui.tabWidget.widget(current_index)
        if not widget:
            return
        scroll: SoftwareBrowserView = [i for i in widget.findChildren(SoftwareBrowserView)][0]

    def add_tab(self, name: str):
        """
            添加tab
        """
        widget_tab = QWidget()
        vbox_tab_main = QVBoxLayout(widget_tab)
        vbox_tab_main.setContentsMargins(0, 0, 0, 0)
        all_software = tuple([i for i in self.software_list if i.tab == name])
        self.scroll_main = SoftwareBrowserView(all_software)
        vbox_tab_main.addWidget(self.scroll_main)
        self.startup_ui.tabWidget.addTab(widget_tab, name)

    def _get_software_browser(self, tab_index: int) -> SoftwareBrowserView:
        widget = self.startup_ui.tabWidget.widget(tab_index)
        return [i for i in widget.findChildren(SoftwareBrowserView)][0]

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
        a0.ignore()
        self.hide()
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "最小化到托盘",
            "应用程序已最小化到系统托盘。",
            QSystemTrayIcon.Information,
            2000
        )

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

    def show(self):
        if self.isMinimized():
            self.showNormal()  # 如果窗口最小化，恢复到正常状态
        super(StartupViewer, self).show()
        self.raise_()  # 将窗口置于顶端
        self.activateWindow()  # 激活窗口

    def on_tray_icon_activated(self, reason):
        """
        处理托盘图标的激活事件。
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
