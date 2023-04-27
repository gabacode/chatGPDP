import markdown2
from PyQt5.QtWidgets import QSizePolicy, QTextEdit, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

from chatgpdp.modules.utils.settings import Settings
from chatgpdp.modules.utils.utilities import Utilities
from chatgpdp.styles.use_style import Style


class MessageBox(QWidget):
    messageChanged = pyqtSignal()
    settings = Settings().get()

    def __init__(self, chatbot, message, mode):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        styles = {
            "author": f"color: {self.colorize(mode, 'label')}; font-weight: bold; margin-left: 5px;",
            "message": f"background-color: {self.colorize(mode, 'background')}; color: {self.colorize(mode, 'foreground')}; border-radius: 25px; border: none;",
        }

        self.author_label = AuthorLabel(mode)
        self.author_label.setStyleSheet(styles["author"])

        self.text_message = Message(chatbot, message)
        self.text_message.messageChanged.connect(self.emit_signal)
        self.text_message.setStyleSheet(styles["message"])

        self.layout.addWidget(self.author_label)
        self.layout.addWidget(self.text_message)

        self.text_message.heightChanged.connect(self.update_height)

    def emit_signal(self):
        self.messageChanged.emit()

    def update_height(self):
        new_height = self.text_message.height() + self.author_label.height() * 2
        self.setFixedHeight(new_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_height()

    def colorize(self, mode, type):
        return self.settings.value(f"colors/{mode}/{type}")


class AuthorLabel(QLabel):
    def __init__(self, mode):
        super().__init__()
        self.setMaximumHeight(20)
        self.setText(Utilities.get_name_from_mode(mode) + ":")


class Message(QTextEdit):
    heightChanged = pyqtSignal()
    messageChanged = pyqtSignal()
    plugins = ["fenced-code-blocks", "codehilite", "tables", "break-on-newline"]
    styles = ""

    def __init__(self, chatbot, message):
        super().__init__()
        self.doc = self.document()
        self.chatbot = chatbot
        self.message = message
        self.is_editing = False
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        Message.styles = Message.styles or self.load_css()

        self.setHtml(self.to_markdown(self.message))

    def to_markdown(self, text):
        md = markdown2.markdown(text, extras=Message.plugins)
        formatted = self.format_code(md)
        return formatted

    def load_css(self):
        style = Style.get_style("markdown.css")
        return style

    def format_code(self, code):
        return f"<style>{Message.styles}</style>{code}" if Message.styles else code

    def resize(self):
        margins = self.contentsMargins()
        height = int(self.doc.size().height() + margins.top() + margins.bottom())
        self.setFixedHeight(height)
        self.heightChanged.emit()

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.setStyleSheet("border: none; border-radius: 0px;")
        index, _ = self.get_message_index()
        if index != 0:
            if self.is_editing:
                menu.addAction(QIcon.fromTheme("document-save"), "Save Message", self.save_message)
            else:
                menu.addAction(QIcon.fromTheme("document-new"), "Edit Message", self.edit_message)
                menu.addAction(QIcon.fromTheme("edit-delete"), "Delete Message", self.delete_message)
        menu.exec_(self.mapToGlobal(event.pos()))

    def edit_message(self):
        index, _ = self.get_message_index()
        original_message = self.chatbot.get_message(index)
        self.is_editing = True
        self.parent().parent().parent().parent().is_editing = True
        self.setPlainText(original_message["content"])
        self.setReadOnly(False)
        self.setAcceptRichText(False)
        self.setStyleSheet(self.styleSheet().replace("border: none;", "border: 2px solid #333;"))
        self.textChanged.connect(self.resize)

    def save_message(self):
        self.is_editing = False
        self.setReadOnly(True)
        self.setStyleSheet(self.styleSheet().replace("border: 2px solid #333;", "border: none;"))

        index, _ = self.get_message_index()
        new_message = self.toPlainText()
        self.setHtml(self.to_markdown(new_message))
        self.chatbot.replace_message(index, new_message)
        self.textChanged.disconnect(self.resize)
        self.messageChanged.emit()
        self.document().setModified(True)

    def delete_message(self):
        index, layout = self.get_message_index()
        if index == 0:
            return
        self.messageChanged.emit()
        self.chatbot.remove_from_history(index)
        layout.takeAt(index).widget().deleteLater()

    def get_message_index(self):
        message_box = self.parentWidget()
        layout = self.parentWidget().parentWidget().layout()
        widget_list = [layout.itemAt(i).widget() for i in range(layout.count())]
        index = widget_list.index(message_box)
        return index, layout

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize()

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
