import sys
from chat import chat
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = "gpt-3.5-turbo-0301"
        self.temperature = 0.618
        self.setWindowTitle("Chat")

        # [CHATLOG]
        self.chat_log = QTextEdit(self)
        self.chat_log.setReadOnly(True)

        # [PROMPT]
        self.prompt = QTextEdit(self)
        self.prompt.setLineWrapMode(QTextEdit.NoWrap)
        self.prompt.textChanged.connect(self.resizeTextEdit)

        # [SEND BUTTON]
        send_button = QPushButton("Send", self)
        send_button.clicked.connect(self.send_message)

        # [EXIT BUTTON]
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.exit_chat)

        # [LAYOUT]
        layout = QVBoxLayout()
        layout.addWidget(self.chat_log)
        layout.addWidget(self.prompt)
        layout.addWidget(send_button)
        layout.addWidget(exit_button)

        # Create widget and init the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.prompt.setFocus()

    def send_message(self):
        message = self.prompt.toPlainText()
        self.chat_log.append("User: " + message + "\n")
        response = chat(message, self.engine, self.temperature)
        self.chat_log.append("Assistant: " + response + "\n")
        self.prompt.clear()
        self.prompt.setFocus()

    def resizeTextEdit(self):
        documentHeight = self.prompt.document().size().height()
        scrollbarHeight = self.prompt.verticalScrollBar().sizeHint().height()
        contentHeight = documentHeight + scrollbarHeight
        self.prompt.setFixedHeight(int(contentHeight))

    def exit_chat(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
