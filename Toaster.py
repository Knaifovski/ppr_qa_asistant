import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import QTimer, Qt

class Toast(QWidget):
    def __init__(self, message):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.ToolTip
        )

        self.label = QLabel(message, self)
        self.label.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 10px;
            border-radius: 8px;
        """)
        self.label.adjustSize()

        self.resize(self.label.size())

        # Позиция (например, центр экрана)
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

        # Закрыть через 1 секунду
        QTimer.singleShot(1000, self.close)

        self.show()
