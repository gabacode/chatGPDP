import os
import sys
from config import engines, options, colors, initial_prompt
from modules.Chatbot import Chatbot

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, pyqtSlot
from PyQt5.QtGui import QDesktopServices, QTextCharFormat, QBrush, QColor, QTextCursor
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMenu,
)
from modules.Utilities import Utilities
from modules.ConfigDialog import ConfigDialog
from modules.PersonalityDialog import PersonalityDialog


chatbot = Chatbot([{"role": "system", "content": initial_prompt}])


class ChatWindow(QMainWindow):
    loading_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.options = Utilities.get_engine_names(engines)
        self.engine = self.engine, *_ = self.options
        self.temperature = 0.618
        self.setWindowTitle("ChatGPDP")
        self.is_loading = False
        self.loading_signal.connect(self.set_loading)

        # [MENU]
        menubar = self.menuBar()

        file_menu = QMenu("File", self)
        options_menu = QMenu("Options", self)
        help_menu = QMenu("Help", self)

        menubar.addMenu(file_menu)
        menubar.addMenu(options_menu)
        menubar.addMenu(help_menu)

        # [NEW CHAT]
        new_action = QAction("New Chat", self)
        new_action.triggered.connect(self.restart_chat)
        file_menu.addAction(new_action)

        # [LOAD CHAT]
        load_action = QAction("Load Chat", self)
        load_action.triggered.connect(self.load_history)
        file_menu.addAction(load_action)

        # [SAVE CHAT]
        save_action = QAction("Save Chat", self)
        save_action.triggered.connect(self.save_history)
        file_menu.addAction(save_action)

        # [EXIT]
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_chat)
        file_menu.addAction(exit_action)

        # [CHANGE PERSONALITY]
        change_personality_action = QAction("Change Personality...", self)
        change_personality_action.triggered.connect(self.change_personality)
        options_menu.addAction(change_personality_action)

        # [SETTINGS]
        set_config_action = QAction("Set API Key...", self)
        set_config_action.triggered.connect(self.show_config_dialog)
        options_menu.addAction(set_config_action)

        # [GET API KEY]
        get_api_key_action = QAction("Get API Key...", self)
        get_api_key_action.triggered.connect(self.get_api_key)
        help_menu.addAction(get_api_key_action)

        # [Go to GitHub]
        github_action = QAction("View Source...", self)
        github_action.triggered.connect(self.go_to_github)
        help_menu.addAction(github_action)

        # [SELECT ENGINE]
        model_label = QLabel("Select a model:", self)
        model_dropdown = QComboBox(self)
        model_dropdown.addItems(self.options)
        model_dropdown.setCurrentIndex(0)
        model_dropdown.activated[str].connect(self.change_engine)

        # [SELECT TEMPERATURE]
        self.temperature_label = QLabel(f"Select a temperature: {self.temperature}", self)
        temperature_slider = QSlider(Qt.Horizontal, self)
        temperature_slider.setMinimum(0)
        temperature_slider.setMaximum(1000)
        temperature_slider.setValue(618)
        temperature_slider.setTickInterval(10)
        temperature_slider.setTickPosition(QSlider.TicksBelow)
        temperature_slider.valueChanged.connect(self.change_temperature)

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
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)

        # [EXIT BUTTON]
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.exit_chat)

        # [LAYOUT]
        layout = QVBoxLayout()
        layout.addWidget(model_label)
        layout.addWidget(model_dropdown)
        layout.addWidget(self.temperature_label)
        layout.addWidget(temperature_slider)
        layout.addWidget(self.chat_log)
        layout.addWidget(self.prompt)
        layout.addWidget(self.send_button)
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

    def change_engine(self, text):
        self.engine = text

    def change_temperature(self, value):
        self.temperature = value / 1000.0
        self.temperature_label.setText(f"Select a temperature: {self.temperature}")

    @pyqtSlot(bool)
    def set_loading(self, is_loading):
        self.is_loading = is_loading
        self.send_button.setEnabled(not is_loading)
        self.send_button.setText("Evaluating..." if is_loading else "Send")

    def append_message(self, mode, message):
        cursor = self.chat_log.textCursor()
        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(colors[mode])))
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"[{mode.capitalize()}]: {message}\n", format)
        cursor.insertText("\n")
        self.chat_log.moveCursor(QTextCursor.End)
        self.chat_log.ensureCursorVisible()

    def send_message(self):
        message = self.prompt.toPlainText()
        self.append_message("user", message)
        self.prompt.clear()

        self.is_loading = True
        self.loading_signal.emit(True)

        if hasattr(self, "chat_thread") and self.chat_thread.isRunning():
            self.chat_thread.terminate()
            self.chat_thread.wait()

        self.chat_thread = ChatThread(message, self.engine, self.temperature)
        self.chat_thread.response_signal.connect(self.handle_response)
        self.chat_thread.start()

    def handle_response(self, response):
        self.append_message("assistant", response)
        self.is_loading = False
        self.loading_signal.emit(False)
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

    def change_personality(self):
        personality_dialog = PersonalityDialog(self)
        if personality_dialog.exec_() == QDialog.Accepted:
            self.restart_chat()

    def restart_chat(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def save_history(self):
        global chatbot
        chatlogs_directory = "chatlogs"
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", chatlogs_directory, "JSON Files (*.json)")
        if file_name:
            history = chatbot.get_history()
            Utilities.save_chat(file_name, history)

    def load_history(self):
        global chatbot
        chatlogs_directory = "chatlogs"
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", chatlogs_directory, "JSON Files (*.json)")
        if file_name:
            history = Utilities.load_chat(file_name)
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

    def get_api_key(self):
        url = QUrl("https://platform.openai.com/account/api-keys")
        QDesktopServices.openUrl(url)

    def go_to_github(self):
        url = QUrl("https://github.com/gabacode/chatGPDP")
        QDesktopServices.openUrl(url)


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
