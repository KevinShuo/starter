import json

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *

from src.config.config import G_version
from src.updater import Updater
from src.views.startup_view import StartupViewer
from src.version import *
import sys


def check_update():
    with open(os.path.join(os.path.dirname(__file__), 'config/version.json'), 'r', encoding="utf-8") as f:
        version_json = json.load(f)
    target_path = version_json["target_path"]
    if not os.path.exists(target_path):
        raise FileNotFoundError
    version_data = check_version(target_path, G_version)
    if not version_data:
        return
    update = Updater()
    src_dir = os.path.dirname(os.path.dirname(__file__))
    update.set_src_path(src_dir)
    update.set_dst_path(target_path)
    update.run()


if __name__ == '__main__':
    print(sys.executable)
    check_update()
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    w = StartupViewer()
    sys.exit(app.exec_())
