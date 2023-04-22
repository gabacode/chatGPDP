import os
import sys

from PyQt5.QtCore import Qt, QEvent, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QFileDialog,
    QSplitter,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMenu,
)

from chatgpdp.modules import ModelSelector, Temperature, Chatbot, MessageBox
from chatgpdp.modules.dialogs import AboutDialog, ConfigDialog, PersonalityDialog
from chatgpdp.modules.utils.config import PATHS, load_initial_prompt, shortcuts
from chatgpdp.modules.utils import Settings, Utilities
from chatgpdp.modules.threads.chat import ChatThread


class ChatWindow(QMainWindow):
    loading_signal = pyqtSignal(bool)
    settings = Settings().get_settings()

    def __init__(self, metadata):
        super().__init__()
        self.metadata = metadata
        self.window_title = f"{metadata['Formal-Name']} v{metadata['Version']}"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.window_title)
        self.initial_prompt = load_initial_prompt()

        geometry_key = "window/geometry"
        geometry = self.settings.value(geometry_key)
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(100, 100, 800, 800)

        initial_prompt_key = "chat/initial_prompt"
        initial_prompt = self.settings.value(initial_prompt_key)
        if initial_prompt:
            self.initial_prompt = initial_prompt
        else:
            self.settings.setValue(initial_prompt_key, self.initial_prompt)

        self.chatbot = Chatbot([{"role": "system", "content": self.initial_prompt}])

        self.temperature = 0.618
        self.opened_file = None
        self.is_loading = False

        self.loading_signal.connect(self.set_loading)

        # [MENU]
        menubar = self.menuBar()
        menu_items = {
            "File": [
                ("New Chat", shortcuts["New"], self.new_chat),
                ("Load Chat", shortcuts["Open"], self.load_history),
                ("Save Chat", shortcuts["Save"], self.save_history),
                ("Save Chat As...", shortcuts["SaveAs"], self.save_history_as),
                ("Exit", shortcuts["Exit"], self.close),
            ],
            "Edit": [
                ("Reload...", shortcuts["Reload"], self.reload_history),
            ],
            "Options": [
                ("Change Personality...", shortcuts["ChangePersonality"], self.change_personality),
                ("Set API Key...", None, self.show_config_dialog),
            ],
            "Help": [
                ("About...", None, self.show_about_dialog),
                ("Get API Key...", None, self.get_api_key),
                ("View Source...", None, self.go_to_github),
            ],
        }
        for menu_title, items in menu_items.items():
            menu = menubar.addMenu(menu_title)
            for label, shortcut, function in items:
                action = QAction(label, self)
                if shortcut:
                    action.setShortcut(shortcut)
                action.triggered.connect(function)
                menu.addAction(action)

        # [SELECT ENGINE]
        model_widget = ModelSelector()
        self.engine = model_widget.get_engine()

        # [SELECT TEMPERATURE]
        temperature_widget = Temperature(self.temperature)

        # [CHATLOG]
        self.conversation_container = QWidget()
        self.conversation_container.setStyleSheet("background-color: #ffffff; border-radius: 5px;")

        self.chat_log_layout = QVBoxLayout(self.conversation_container)
        self.chat_log_layout.setAlignment(Qt.AlignTop)
        self.chat_log_layout.setContentsMargins(0, 10, 0, 10)

        self.chat_log = QScrollArea(widgetResizable=True)
        self.chat_log.setWidget(self.conversation_container)

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
            model_widget,
            temperature_widget,
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
        message = message.strip()
        message_widget = MessageBox(self.chatbot, message, mode)
        message_widget.messageChanged.connect(self.set_to_save)
        self.chat_log_layout.addWidget(message_widget)
        self.chat_log_layout.update()
        self.scroll_to_bottom(message_widget.height())

    def set_to_save(self):
        self.setWindowTitle(
            f"{self.window_title} - {Utilities.path_strip(self.opened_file)}*"
            if self.opened_file
            else f"{self.window_title} - New Chat*"
        )

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
        self.set_to_save()
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
        self.new_window = ChatWindow(self.metadata)
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
        new_file, _ = QFileDialog.getSaveFileName(self, "Save File", PATHS["chatlogs"], file_filter)
        if not new_file:
            return
        file_name = Utilities.save_chat(new_file, self.chatbot.history)
        if file_name:
            self.set_opened_file(file_name)

    def load_history(self):
        file_filter = "JSON Files (*.json)"
        loaded_file, _ = QFileDialog.getOpenFileName(self, "Open File", PATHS["chatlogs"], file_filter)
        if loaded_file:
            history = Utilities.load_chat(loaded_file)
            for i in reversed(range(self.chat_log_layout.count())):
                self.chat_log_layout.itemAt(i).widget().setParent(None)
            self.chatbot = Chatbot(history)
            for message in history:
                self.append_message(message["role"], message["content"])
            self.set_opened_file(loaded_file)

    def reload_history(self):
        if self.opened_file:
            history = Utilities.load_chat(self.opened_file)
            for i in reversed(range(self.chat_log_layout.count())):
                self.chat_log_layout.itemAt(i).widget().setParent(None)
            self.chatbot = Chatbot(history)
            for message in history:
                self.append_message(message["role"], message["content"])

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Exit", "Do you want to save the chat history?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if reply == QMessageBox.Yes:
            self.save_history()
        elif reply == QMessageBox.Cancel:
            event.ignore()
            return
        self.settings.setValue("window/geometry", self.saveGeometry())
        event.accept()

    def get_api_key(self):
        url = "https://platform.openai.com/account/api-keys"
        Utilities.open_link(url)

    def go_to_github(self):
        url = "https://github.com/gabacode/chatGPDP"
        Utilities.open_link(url)
