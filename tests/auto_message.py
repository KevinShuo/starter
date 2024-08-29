import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation


class AutoDismissMessage(QLabel):
    def __init__(self, parent=None, message="", msg_type="info", duration=3000):
        super().__init__(parent)

        # 设置提示框的样式和文本
        self.setText(message)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(200, 50)  # 设置固定大小
        self.setStyleSheet(self.get_style(msg_type))

        # 设置提示框在父窗口上方居中
        self.move_to_top_center()

        # 设置一个定时器，在指定时间后开始淡出效果
        QTimer.singleShot(duration, self.start_fade_out)

    def get_style(self, msg_type):
        """返回不同类型的提示框样式."""
        if msg_type == "info":
            return "background-color: lightblue; border: 1px solid black;"
        elif msg_type == "warning":
            return "background-color: yellow; border: 1px solid black;"
        elif msg_type == "critical":
            return "background-color: red; border: 1px solid black; color: white;"
        else:
            return "background-color: lightgray; border: 1px solid black;"

    def move_to_top_center(self):
        """将提示框移动到父窗口的顶部中央位置."""
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = (parent_geometry.width() - self.width()) // 2
            y = 30  # 设置提示框距离主窗口顶部的距离
            self.move(x, y)

    def start_fade_out(self):
        """开始淡出效果的动画."""
        # 创建透明度效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # 创建透明度动画
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)  # 设置动画持续时间为1秒
        self.fade_animation.setStartValue(1)  # 从不透明开始
        self.fade_animation.setEndValue(0)  # 到完全透明结束

        # 在动画结束时关闭提示框
        self.fade_animation.finished.connect(self.close)

        # 开始动画
        self.fade_animation.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口的大小和标题
        self.setWindowTitle("Auto-Dismiss Message with Fade-Out Effect")
        self.setGeometry(100, 100, 400, 300)

        # 显示不同类型的消息提示框
        # self.show_message("这是信息提示", "info")
        self.show_message("这是警告提示", "warning", 4000)  # 4秒后淡出
        # self.show_message("这是严重错误提示", "critical", 5000)  # 5秒后淡出

    def show_message(self, message, msg_type, duration=3000):
        # 创建并显示消息提示框
        message_box = AutoDismissMessage(self, message, msg_type, duration)
        message_box.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())