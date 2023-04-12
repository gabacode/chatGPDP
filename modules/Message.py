from PyQt5.QtWidgets import QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt


class MessageBox(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setAcceptRichText(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
