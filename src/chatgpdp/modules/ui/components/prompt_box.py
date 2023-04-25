from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, QEvent


class PromptBox(QTextEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup()

    def setup(self):
        self.setAcceptRichText(False)
        self.setPlaceholderText("Type your message here... (Press Shift+ENTER to start a new line)")
        self.installEventFilter(self)
        self.textChanged.connect(self.resize_prompt)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self:
            if event.key() == Qt.Key_Return and self.hasFocus():
                if event.modifiers() == Qt.ShiftModifier:
                    self.textCursor().insertText("\n")
                else:
                    self.parent.send_message()
                return True
        return super().eventFilter(obj, event)

    def resize_prompt(self):
        documentHeight = self.document().size().height()
        scrollbarHeight = self.verticalScrollBar().sizeHint().height()
        contentHeight = documentHeight + scrollbarHeight
        self.parent.divider.setSizes([int(self.parent.divider.height() - contentHeight), int(contentHeight)])
