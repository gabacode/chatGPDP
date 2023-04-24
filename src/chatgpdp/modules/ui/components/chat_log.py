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
        self.scroll_to_bottom(message_widget.height())

    def clear(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

    def scroll_to_bottom(self, message_height):
        this_max = self.verticalScrollBar().maximum()
        new_max = this_max + message_height
        self.verticalScrollBar().setMaximum(new_max)
        self.verticalScrollBar().setValue(new_max)
