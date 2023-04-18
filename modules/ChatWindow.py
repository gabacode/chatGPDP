import os
import sys
from config import chatlogs_directory, colors, engines, load_initial_prompt, shortcuts, version
from modules.Chatbot import Chatbot

from PyQt5.QtCore import Qt, QEvent, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QAction,
    QComboBox,
    QDialog,
    QFileDialog,
    QSplitter,
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
from modules.Message import MessageBox
from modules.Utilities import Utilities
from modules.dialogs.AboutDialog import AboutDialog
from modules.dialogs.ConfigDialog import ConfigDialog
from modules.dialogs.PersonalityDialog import PersonalityDialog
from threads.ChatThread import ChatThread


class ChatWindow(QMainWindow):
    window_title = "ChatGPDP" + " v" + version
    loading_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.window_title)

        self.initial_prompt = load_initial_prompt()
        self.chatbot = Chatbot([{"role": "system", "content": self.initial_prompt}])

        self.opened_file = None
        self.is_loading = False
        self.loading_signal.connect(self.set_loading)

        self.options = Utilities.get_engine_names(engines)
        self.engine = self.engine, *_ = self.options
        self.temperature = 0.618

        # [MENU]
        menubar = self.menuBar()

        file_menu = QMenu("File", self)
        edit_menu = QMenu("Edit", self)
        options_menu = QMenu("Options", self)
        help_menu = QMenu("Help", self)

        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        menubar.addMenu(options_menu)
        menubar.addMenu(help_menu)

        menu_items = {
            "file": [
                {"label": "New Chat", "function": self.new_chat, "shortcut": shortcuts["New"]},
                {"label": "Load Chat", "function": self.load_history, "shortcut": shortcuts["Open"]},
                {"label": "Save Chat", "function": self.save_history, "shortcut": shortcuts["Save"]},
                {"label": "Save Chat As...", "function": self.save_history_as, "shortcut": shortcuts["SaveAs"]},
                {"label": "Exit", "function": self.close, "shortcut": shortcuts["Exit"]},
            ],
            "edit": [
                {
                    "label": "Reload...",
                    "function": self.reload_history,
                    "shortcut": shortcuts["Reload"],
                },
            ],
            "options": [
                {
                    "label": "Change Personality...",
                    "function": self.change_personality,
                    "shortcut": shortcuts["ChangePersonality"],
                },
                {"label": "Set API Key...", "function": self.show_config_dialog},
            ],
            "help": [
                {"label": "About...", "function": self.show_about_dialog},
                {"label": "Get API Key...", "function": self.get_api_key},
                {"label": "View Source...", "function": self.go_to_github},
            ],
        }

        self.create_menu(file_menu, menu_items["file"])
        self.create_menu(edit_menu, menu_items["edit"])
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
        self.chat_log_widget = QWidget()
        self.chat_log_widget.setStyleSheet("background-color: #ffffff; border-radius: 5px;")
        self.chat_log_layout = QVBoxLayout(self.chat_log_widget)
        self.chat_log_layout.setAlignment(Qt.AlignTop)
        self.chat_log = QScrollArea(widgetResizable=True)
        self.chat_log.setWidget(self.chat_log_widget)

        # [PROMPT]
        self.prompt = QTextEdit(self)
        self.prompt.setAcceptRichText(False)
        self.prompt.setPlaceholderText("Type your message here... (Press Shift+ENTER to start a new line)")
        self.prompt.installEventFilter(self)
        self.prompt.textChanged.connect(self.resize_prompt)

        # [DIVIDER]
        self.divider = QSplitter(Qt.Vertical)
        self.divider.addWidget(self.chat_log)
        self.divider.addWidget(self.prompt)
        self.divider.setSizes([300, 100])
        self.divider.setCollapsible(0, False)
        self.divider.setCollapsible(1, False)

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
            self.divider,
            self.send_button,
        ]
        for widget in widgets:
            layout.addWidget(widget)

        # Create widget and init the layout
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.append_message("system", self.initial_prompt)
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
        author_height, label_height = 20, 20
        message = message.strip()

        author_widget = QLabel()
        author_widget.setMaximumHeight(author_height)

        author_widget.setText(Utilities.get_name_from_mode(mode) + ":")
        author_widget.setStyleSheet(f"color: {colors[mode]['foreground']}; font-weight: bold; margin-left: 5px;")
        self.chat_log_layout.addWidget(author_widget)

        message_widget = MessageBox(message, mode)
        self.chat_log_layout.addWidget(message_widget)

        space_label = QLabel()
        space_label.setMaximumHeight(label_height)
        self.chat_log_layout.addWidget(space_label)

        self.scroll_to_bottom(author_height + message_widget.height() + label_height)

    def scroll_to_bottom(self, message_height):
        self.chat_log.verticalScrollBar().setMaximum(self.chat_log.verticalScrollBar().maximum() + message_height)
        self.chat_log.verticalScrollBar().setValue(self.chat_log.verticalScrollBar().maximum())

    def send_message(self):
        message = self.prompt.toPlainText()
        if message.strip() == "":
            self.prompt.setText("")
            self.prompt.setFocus()
            return
        self.append_message("user", message)
        self.setWindowTitle(
            f"{self.window_title} - {Utilities.path_strip(self.opened_file)}*"
            if self.opened_file
            else f"{self.window_title} - New Chat*"
        )
        self.prompt.clear()

        self.is_loading = True
        self.loading_signal.emit(True)

        if hasattr(self, "chat_thread") and self.chat_thread.isRunning():
            self.chat_thread.terminate()
            self.chat_thread.wait()

        self.chat_thread = ChatThread(self.chatbot, message, self.engine, self.temperature)
        self.chat_thread.response_signal.connect(self.handle_response)
        self.chat_thread.start()

    def handle_response(self, response):
        self.append_message("assistant", response)
        self.is_loading = False
        self.loading_signal.emit(False)
        self.prompt.setFocus()

    def resize_prompt(self):
        documentHeight = self.prompt.document().size().height()
        scrollbarHeight = self.prompt.verticalScrollBar().sizeHint().height()
        contentHeight = documentHeight + scrollbarHeight
        self.divider.setSizes([int(self.divider.height() - contentHeight), int(contentHeight)])

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
            self.close()
            self.new_chat()

    def new_chat(self):
        self.new_window = ChatWindow()
        self.new_window.setGeometry(100, 100, 800, 800)
        self.new_window.show()

    def restart_chat(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def set_opened_file(self, file_name):
        self.opened_file = file_name
        self.setWindowTitle(f"{self.window_title} - {Utilities.path_strip(file_name)}")

    def save_history(self):
        if self.opened_file:
            file_name = Utilities.save_chat(self.opened_file, self.chatbot.history)
            self.set_opened_file(file_name if file_name else self.opened_file)
        else:
            self.save_history_as()

    def save_history_as(self):
        file_filter = "JSON Files (*.json)"
        new_file, _ = QFileDialog.getSaveFileName(self, "Save File", chatlogs_directory, file_filter)
        if not new_file:
            return
        file_name = Utilities.save_chat(new_file, self.chatbot.history)
        if file_name:
            self.set_opened_file(file_name)

    def load_history(self):
        file_filter = "JSON Files (*.json)"
        loaded_file, _ = QFileDialog.getOpenFileName(self, "Open File", chatlogs_directory, file_filter)
        if loaded_file:
            history = Utilities.load_chat(loaded_file)
            for i in reversed(range(self.chat_log_layout.count())):
                self.chat_log_layout.itemAt(i).widget().setParent(None)
            for message in history:
                self.append_message(message["role"], message["content"])
            self.set_opened_file(loaded_file)
            self.chatbot = Chatbot(history)

    def reload_history(self):
        if self.opened_file:
            history = Utilities.load_chat(self.opened_file)
            for i in reversed(range(self.chat_log_layout.count())):
                self.chat_log_layout.itemAt(i).widget().setParent(None)
            for message in history:
                self.append_message(message["role"], message["content"])
            self.chatbot = Chatbot(history)

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
        url = "https://platform.openai.com/account/api-keys"
        Utilities.open_link(url)

    def go_to_github(self):
        url = "https://github.com/gabacode/chatGPDP"
        Utilities.open_link(url)
