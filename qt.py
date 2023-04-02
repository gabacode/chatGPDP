import os
import sys
from chat import chat
from config import options
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QDialogButtonBox,
    QWidget,
)


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.env_path = ".env"
        self.setWindowTitle("Configuration")
        self.setFixedWidth(600)
        layout = QVBoxLayout(self)

        # Add the options
        options = self.read_env()
        for option in options:
            option_label = QLabel(option[0])
            option_edit = QLineEdit(option[1])
            layout.addWidget(option_label)
            layout.addWidget(option_edit)

        # Add the buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def init_env(self):
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=")

    def read_env(self):
        self.init_env()
        options = []
        with open(self.env_path, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                options.append((key, value))
        return options

    def write_env(self):
        updated_options = []
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                key = widget.parent().findChild(QLabel).text()
                value = widget.text()
                updated_options.append((key, value))
        with open(self.env_path, "w") as f:
            for option in updated_options:
                f.write(f"{option[0]}={option[1]}\n")


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = "gpt-3.5-turbo-0301"
        self.temperature = 0.618
        self.setWindowTitle("Chat")

        # [MENU]
        menubar = self.menuBar()

        # [OPTIONS]
        options_menu = QMenu("Menu", self)
        menubar.addMenu(options_menu)

        # [CONFIG]
        set_config_action = QAction("Configuration", self)
        set_config_action.triggered.connect(self.show_config_dialog)
        options_menu.addAction(set_config_action)

        # [EXIT]
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_chat)
        options_menu.addAction(exit_action)

        # [CHATLOG]
        self.chat_log = QTextEdit(self)
        self.chat_log.setFont(options["default_font"])
        self.chat_log.setStyleSheet(options["styles"]["box"])
        self.chat_log.setReadOnly(True)

        # [PROMPT]
        self.prompt = QTextEdit(self)
        self.prompt.setAcceptRichText(False)
        self.prompt.setPlaceholderText("Type your message here...")
        self.prompt.setFont(options["default_font"])
        self.prompt.setStyleSheet(options["styles"]["box"])
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

    def show_config_dialog(self):
        config_dialog = ConfigDialog(self)
        if config_dialog.exec_() == QDialog.Accepted:
            config_dialog.write_env()
        else:
            config_dialog.close()

    def exit_chat(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
