import os, sys
from chat import Chatbot
from config import options, colors, initial_prompt

from PyQt5.QtGui import QTextCharFormat, QBrush, QColor

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QMenu,
    QFileDialog,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QScrollArea,
    QWidget,
)
from utils import load_history

from widgets.ConfigDialog import ConfigDialog

chatbot = Chatbot([{"role": "system", "content": initial_prompt}])


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

        # [LOAD]
        load_action = QAction("Load Chat", self)
        load_action.triggered.connect(self.load_history)
        options_menu.addAction(load_action)

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
        self.chat_log.verticalScrollBar().setStyleSheet(options["styles"]["scroll_bar_vertical"])
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
        send_button.setEnabled(not chatbot.is_thinking)
        send_button.clicked.connect(self.send_message)

        # [RESTART BUTTON]
        restart_button = QPushButton("Restart", self)
        restart_button.clicked.connect(self.restart_chat)

        # [EXIT BUTTON]
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.exit_chat)

        # [LAYOUT]
        layout = QVBoxLayout()
        layout.addWidget(self.chat_log)
        layout.addWidget(self.prompt)
        layout.addWidget(send_button)
        layout.addWidget(restart_button)
        layout.addWidget(exit_button)

        # [SCROLL AREA]
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(layout)

        # Create widget and init the layout
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(scroll_area)
        self.setCentralWidget(widget)
        self.prompt.setFocus()

    def append_message(self, mode, message):
        cursor = self.chat_log.textCursor()
        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(colors[mode])))
        if mode == "user":
            cursor.insertText("User: " + message + "\n", format)
        elif mode == "assistant":
            cursor.insertText("Assistant: " + message + "\n", format)
        cursor.insertText("\n")
        self.chat_log.setTextCursor(cursor)
        self.chat_log.ensureCursorVisible()

    def send_message(self):
        message = self.prompt.toPlainText()
        self.append_message("user", message)
        self.prompt.clear()

        if hasattr(self, "chat_thread") and self.chat_thread.isRunning():
            self.chat_thread.terminate()
            self.chat_thread.wait()

        self.chat_thread = ChatThread(message, self.engine, self.temperature)
        self.chat_thread.response_signal.connect(self.handle_response)
        self.chat_thread.start()

    def handle_response(self, response):
        self.append_message("assistant", response)
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

    def restart_chat(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def load_history(self):
        global chatbot
        chatlogs_directory = "chatlogs"
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", chatlogs_directory, "JSON Files (*.json)")
        if file_name:
            history = load_history(file_name)
            self.chat_log.clear()
            for message in history:
                if message["role"] == "user":
                    self.append_message("user", message["content"])
                elif message["role"] == "assistant":
                    self.append_message("assistant", message["content"])
                elif message["role"] == "system":
                    self.append_message("system", message["content"])
            chatbot = Chatbot(history)

    def exit_chat(self):
        self.close()


class ChatThread(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, message, engine, temperature):
        super().__init__()
        self.message = message
        self.engine = engine
        self.temperature = temperature

    def run(self):
        response = chatbot.chat(self.message, self.engine, self.temperature)
        self.response_signal.emit(response)
