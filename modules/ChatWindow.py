import os
import sys
from config import chatlogs_directory, colors, engines, initial_prompt, shortcuts, version
from modules.Chatbot import Chatbot

from PyQt5.QtCore import Qt, QEvent, QThread, QTimer, pyqtSignal, QUrl, pyqtSlot
from PyQt5.QtGui import (
    QDesktopServices,
    QFont,
    QTextCharFormat,
    QBrush,
    QColor,
    QTextCursor,
    QCursor,
)
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMenu,
)
from modules.Utilities import Utilities
from modules.dialogs.AboutDialog import AboutDialog
from modules.dialogs.ConfigDialog import ConfigDialog
from modules.dialogs.PersonalityDialog import PersonalityDialog


chatbot = Chatbot([{"role": "system", "content": initial_prompt}])


class ChatWindow(QMainWindow):
    loading_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.window_title = "ChatGPDP" + " v" + version
        self.setWindowTitle(self.window_title)

        self.opened_file = None
        self.is_loading = False
        self.loading_signal.connect(self.set_loading)

        self.options = Utilities.get_engine_names(engines)
        self.engine = self.engine, *_ = self.options
        self.temperature = 0.618

        # [MENU]
        menubar = self.menuBar()

        file_menu = QMenu("File", self)
        options_menu = QMenu("Options", self)
        help_menu = QMenu("Help", self)

        menubar.addMenu(file_menu)
        menubar.addMenu(options_menu)
        menubar.addMenu(help_menu)

        menu_items = {
            "file": [
                {"label": "New Chat", "function": self.restart_chat, "shortcut": shortcuts["New"]},
                {"label": "Load Chat", "function": self.load_history, "shortcut": shortcuts["Open"]},
                {"label": "Save Chat", "function": self.save_history, "shortcut": shortcuts["Save"]},
                {"label": "Save Chat As...", "function": self.save_history_as, "shortcut": shortcuts["SaveAs"]},
                {"label": "Exit", "function": self.close, "shortcut": shortcuts["Exit"]},
            ],
            "options": [
                {"label": "Change Personality...", "function": self.change_personality},
                {"label": "Set API Key...", "function": self.show_config_dialog},
            ],
            "help": [
                {"label": "About...", "function": self.show_about_dialog},
                {"label": "Get API Key...", "function": self.get_api_key},
                {"label": "View Source...", "function": self.go_to_github},
            ],
        }

        self.create_menu(file_menu, menu_items["file"])
        self.create_menu(options_menu, menu_items["options"])
        self.create_menu(help_menu, menu_items["help"])

        # [SELECT ENGINE]
        model_label = QLabel("Select a model:", self)
        model_dropdown = QComboBox(self)
        model_dropdown.addItems(self.options)
        model_dropdown.setCurrentIndex(0)
        model_dropdown.activated[str].connect(self.change_engine)

        # [SELECT TEMPERATURE]
        self.temperature_label = QLabel(f"Select a temperature: {self.temperature}", self)
        temperature_slider = QSlider(
            Qt.Horizontal, self, minimum=0, maximum=1000, value=618, tickInterval=10, tickPosition=QSlider.TicksBelow
        )
        temperature_slider.valueChanged.connect(self.change_temperature)

        # [CHATLOG]
        self.chat_log = QTextEdit(self)
        self.chat_log.setReadOnly(True)

        # [PROMPT]
        self.prompt = QTextEdit(self)
        self.prompt.setAcceptRichText(False)
        self.prompt.setPlaceholderText("Type your message here... (Press Shift+ENTER to start a new line)")
        self.prompt.textChanged.connect(self.resizeTextEdit)
        self.prompt.installEventFilter(self)

        # [SEND BUTTON]
        self.send_button = QPushButton("Send", self)
        self.send_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.send_button.clicked.connect(self.send_message)

        # [LAYOUT]
        layout = QVBoxLayout()
        widgets = [
            model_label,
            model_dropdown,
            self.temperature_label,
            temperature_slider,
            self.chat_log,
            self.prompt,
            self.send_button,
        ]
        for widget in widgets:
            layout.addWidget(widget)

        # [SCROLL AREA]
        scroll_area = QScrollArea(widgetResizable=True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(layout)

        # Create widget and init the layout
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(scroll_area)

        self.setCentralWidget(widget)
        self.append_message("system", initial_prompt)
        self.prompt.setFocus()

    def create_menu(self, menu, menu_items):
        for item in menu_items:
            action = QAction(item["label"], self)
            if "shortcut" in item:
                action.setShortcut(item["shortcut"])
            action.triggered.connect(item["function"])
            menu.addAction(action)

    def change_engine(self, text):
        self.engine = text

    def change_temperature(self, value):
        self.temperature = value / 1000.0
        self.temperature_label.setText(f"Change temperature: {self.temperature}")

    @pyqtSlot(bool)
    def set_loading(self, is_loading):
        self.is_loading = is_loading
        self.send_button.setEnabled(not is_loading)
        if is_loading:
            self.loading_text, self.loading_index, self.loading_timer = "  Thinking", 0, QTimer()
            self.loading_timer.timeout.connect(self.update_loading_text)
            self.loading_timer.start(136)
        else:
            self.send_button.setText("Send")
            self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.loading_timer.stop()

    def update_loading_text(self):
        self.loading_index = (self.loading_index + 1) % 4
        self.send_button.setText(f"{self.loading_text}{'.' * self.loading_index}{' ' * (3 - self.loading_index)}")

    def append_message(self, mode, message):
        cursor = self.chat_log.textCursor()
        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(colors[mode])))
        format.setFontWeight(QFont.DemiBold)
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"[{mode.capitalize()}]: {message}\n", format)
        cursor.insertText("\n")
        self.chat_log.moveCursor(QTextCursor.End)
        self.chat_log.ensureCursorVisible()

    def send_message(self):
        message = self.prompt.toPlainText()
        self.append_message("user", message)
        if self.opened_file is not None:
            self.setWindowTitle(f"ChatGPDP - {self.opened_file.split('/')[-1]}*")
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

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.prompt:
            if event.key() == Qt.Key_Return and self.prompt.hasFocus():
                if event.modifiers() == Qt.ShiftModifier:
                    self.prompt.textCursor().insertText("\n")
                else:
                    self.send_message()
                return True
        return super().eventFilter(obj, event)

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

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

    def set_opened_file(self, file_name):
        self.opened_file = file_name
        self.setWindowTitle(f"ChatGPDP - {file_name.split('/')[-1]}")

    def save_history(self):
        global chatbot
        if self.opened_file:
            Utilities.save_chat(self.opened_file, chatbot.history)
            self.set_opened_file(self.opened_file)
        else:
            self.save_history_as()

    def save_history_as(self):
        global chatbot
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", chatlogs_directory, "JSON Files (*.json)")
        if file_name:
            Utilities.save_chat(file_name, chatbot.history)
            self.set_opened_file(file_name)

    def load_history(self):
        global chatbot
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", chatlogs_directory, "JSON Files (*.json)")
        if file_name:
            history = Utilities.load_chat(file_name)
            self.chat_log.clear()
            for message in history:
                self.append_message(message["role"], message["content"])
            self.set_opened_file(file_name)
            chatbot = Chatbot(history)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Exit", "Do you want to save the chat history?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if reply == QMessageBox.Yes:
            self.save_history()
        elif reply == QMessageBox.Cancel:
            event.ignore()
            return
        event.accept()

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
