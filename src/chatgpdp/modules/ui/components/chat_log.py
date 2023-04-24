from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
)

from chatgpdp.modules.chat.message import MessageBox


class ChatLog(QScrollArea):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWidgetResizable(True)
        scrollbar = self.verticalScrollBar()
        scrollbar.rangeChanged.connect(self.scroll_to_bottom)

        self.container = QWidget()
        self.container.setObjectName("conversation_container")

        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 10, 0, 10)

        self.setWidget(self.container)

    def append_message(self, mode, message):
        message = message.strip()
        message_widget = MessageBox(self.parent.chatbot, message, mode)
        message_widget.messageChanged.connect(self.parent.set_to_save)
        self.layout.addWidget(message_widget)

    def clear(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

    def scroll_to_bottom(self):
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
