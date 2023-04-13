from config import colors
from PyQt5.QtWidgets import QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt


class MessageBox(QTextEdit):
    def __init__(self, message, mode):
        super().__init__()
        self.message = message
        self.mode = mode

        self.setReadOnly(True)
        self.setAcceptRichText(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setStyleSheet(f"background-color: {colors[mode]}; color: #F0F0F0;")
        self.setText(message) if mode == "user" else self.setMarkdown(message)
        self.setAlignment(Qt.AlignRight if mode == "user" else Qt.AlignLeft)

        self.textChanged.connect(self.autoResize)

    def wheelEvent(self, event):
        event.ignore()

    def autoResize(self):
        self.document().setTextWidth(self.viewport().width())
        margins = self.contentsMargins()
        height = int(self.document().size().height() + margins.top() + margins.bottom()) + 8
        self.setFixedHeight(height)
        self.update()

    def resizeEvent(self, event):
        self.autoResize()
