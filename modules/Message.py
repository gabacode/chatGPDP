from config import colors
from PyQt5.QtWidgets import QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt

from modules.Utilities import Utilities


class MessageBox(QTextEdit):
    def __init__(self, message, mode):
        super().__init__()
        self.message = message
        self.mode = mode
        self.view = self.viewport()
        self.doc = self.document()

        styles = f"background-color: {colors[mode]['background']}; color: {colors[mode]['foreground']}; border-radius: 25px; border: none;"

        self.setReadOnly(True)
        self.setAcceptRichText(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setStyleSheet(styles)
        self.setText(message) if mode == "user" else self.setMarkdown(message)

        self.textChanged.connect(self.autoResize)

    def wheelEvent(self, event):
        event.ignore()

    def autoResize(self):
        self.doc.setTextWidth(self.viewport().width())
        margins = self.contentsMargins()
        height = int(self.doc.size().height() + margins.top() + margins.bottom()) + 8
        self.setFixedHeight(height)
        self.update()

    def resizeEvent(self, event):
        self.autoResize()

    def mouseMoveEvent(self, event):
        anchor = self.anchorAt(event.pos())
        if anchor:
            self.view.setCursor(Qt.PointingHandCursor)
        else:
            self.view.setCursor(Qt.IBeamCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        anchor = self.anchorAt(event.pos())
        if anchor:
            Utilities.open_link(anchor)
        super().mouseReleaseEvent(event)
