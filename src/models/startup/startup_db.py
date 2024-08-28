import sqlite3
import os
import sys

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication

from .software_dataclass import SoftwareData


class StartupDB:
    def __init__(self, db_path: str):
        self._db_path = db_path
        if not self._db_path.endswith(".db"):
            raise AttributeError("db_path must end with '.db'")
        p = os.path.dirname(self._db_path)
        if not os.path.exists(p):
            try:
                os.makedirs(p)
            except:
                QMessageBox.critical(None, 'Error', f'Could not create the database: {p}',
                                     QMessageBox.StandardButton.Yes)
                app = QApplication.instance()
                app.deleteLater()
                sys.exit(0)
        self._db = sqlite3.connect(self._db_path)
        self._table_name = None

    def initialize(self, table_name: str = "software"):
        """初始化数据库并创建表格"""
        self.table_name = table_name
        self.create_table()
        if not self.get_software():
            self._add_default_software()
        return table_name

    def _add_default_software(self):
        """
            添加默认软件
        Returns:

        """
        default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/default.py")).replace(
            '\\', '/')
        default_ico = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/python.png")).replace(
            '\\', '/')
        self.add_software(name="Hello World", path=default_path, ico=default_ico, tab="default")

    def add_software(self, name: str, path: str, ico: str, tab: str):
        if self._check_exists(name):
            return
        with self._db:
            cursor = self._db.cursor()
            cursor.execute(f''' INSERT INTO {self.table_name} (name, path, ico, tab) VALUES (?, ?, ?, ?)''',
                           (name, path, ico, tab))
            self._db.commit()

    def _check_exists(self, name) -> bool:
        with self._db:
            cursor = self._db.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?", (name,))
            rows = cursor.fetchall()
            if not rows:
                return False
            return True

    def get_software(self):
        with self._db:
            cursor = self._db.cursor()
            cursor.execute(f'''SELECT * FROM {self.table_name}''')
            rows = cursor.fetchall()
            return [SoftwareData(*i) for i in rows]

    def create_table(self):
        """检查表格是否存在，并创建表格"""
        cursor = self._db.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
        table_exists = cursor.fetchone()
        if not table_exists:
            cursor.execute(f'''
create table {self.table_name}
(
    id   integer not null
        constraint {self.table_name}_pk
            primary key,
    name TEXT,
    path TEXT,
    ico  TEXT,
    tab  TEXT
);
 ''')
            self._db.commit()

    def get_all_tables(self):
        with self._db:
            cursor = self._db.cursor()
            cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table';")
            rows = cursor.fetchall()
            return tuple(sorted([i[1] for i in rows]))

    def close(self):
        """关闭数据库连接"""
        if self._db:
            self._db.close()

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, value: str):
        self._table_name = value
