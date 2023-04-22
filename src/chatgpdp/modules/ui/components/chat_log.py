from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGroupBox

class ChatLog(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.conversation_container = QWidget()
        self.conversation_container.setStyleSheet("background-color: #ffffff; border-radius: 5px;")

        self.chat_log_layout = QVBoxLayout(self.conversation_container)
        self.chat_log_layout.setAlignment(Qt.AlignTop)
        self.chat_log_layout.setContentsMargins(0, 10, 0, 10)

        self.chat_log = QScrollArea(widgetResizable=True)
        self.chat_log.setWidget(self.conversation_container)

        chat_log_layout = QVBoxLayout()
        chat_log_layout.addWidget(self.chat_log)
        self.setLayout(chat_log_layout)

        