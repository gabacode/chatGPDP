from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton


class SendButton(QPushButton):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setText("Send")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.parent.send_message)
