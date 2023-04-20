from config import colors
import markdown2
from PyQt5.QtWidgets import QSizePolicy, QTextEdit, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from modules.Utilities import Utilities


class MessageBox(QWidget):
    def __init__(self, message, mode):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        styles = {
            "author": f"color: {colors[mode]['foreground']}; font-weight: bold; margin-left: 5px;",
            "message": f"background-color: {colors[mode]['background']}; color: {colors[mode]['foreground']}; border-radius: 25px; border: none;",
        }

        self.author_label = AuthorLabel(mode)
        self.author_label.setStyleSheet(styles["author"])

        self.text_message = Message(message, mode)
        self.text_message.setStyleSheet(styles["message"])

        self.layout.addWidget(self.author_label)
        self.layout.addWidget(self.text_message)

        self.text_message.heightChanged.connect(self.update_height)

    def update_height(self):
        new_height = self.text_message.height() + self.author_label.height() * 2
        self.setFixedHeight(new_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_height()


class AuthorLabel(QLabel):
    def __init__(self, mode):
        super().__init__()
        self.setMaximumHeight(20)
        self.setText(Utilities.get_name_from_mode(mode) + ":")


class Message(QTextEdit):
    heightChanged = pyqtSignal()

    def __init__(self, message, mode):
        super().__init__()
        self.doc = self.document()
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        html = markdown2.markdown(message, extras=["fenced-code-blocks", "codehilite", "tables"])
        self.setHtml(self.format_code(html))

    def format_code(self, code):
        try:
            with open("styles/markdown.css") as f:
                style = f.read()
                return f"<style>{style}</style>{code}"
        except Exception as e:
            print(e)
            return code

    def resize(self):
        margins = self.contentsMargins()
        height = int(self.doc.size().height() + margins.top() + margins.bottom()) + 8
        self.setFixedHeight(height)
        self.heightChanged.emit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        widgets = self.parentWidget()
        print(widgets)
        print(self)

    def mouseMoveEvent(self, event):
        view = self.viewport()
        anchor = self.anchorAt(event.pos())
        if anchor:
            view.setCursor(Qt.PointingHandCursor)
        else:
            view.setCursor(Qt.IBeamCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        anchor = self.anchorAt(event.pos())
        if anchor:
            Utilities.open_link(anchor)
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        event.ignore()
