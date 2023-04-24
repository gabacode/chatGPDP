import os
import sys

from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from chatgpdp.modules import ModelSelector, Temperature, Chatbot
from chatgpdp.modules.dialogs import AboutDialog, ConfigDialog, PersonalityDialog
from chatgpdp.modules.ui.components import MenuBar, ChatLog, Divider, Prompt, SendButton
from chatgpdp.modules.utils.config import PATHS, load_initial_prompt, shortcuts
from chatgpdp.modules.utils import Settings, Utilities
from chatgpdp.modules.threads.chat import ChatThread


class ChatWindow(QMainWindow):
    loading_signal = pyqtSignal(bool)
    settings = Settings().get_settings()
    default_window_geometry = (100, 100, 800, 800)

    def __init__(self, metadata):
        super().__init__()
        self.metadata = metadata
        self.window_title = f"{metadata['Formal-Name']} v{metadata['Version']}"

        self.load_state()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.window_title)
        self.setMenuBar(MenuBar(self, shortcuts))

        model_selector = ModelSelector()
        self.engine = model_selector.get_engine()

        temperature_selector = Temperature(self.temperature)

        self.chat_log = ChatLog(self)
        self.prompt = Prompt(self)
        self.divider = Divider(self, self.chat_log, self.prompt)

        self.send_button = SendButton(on_click=self.send_message)

        layout = QVBoxLayout()
        widgets = [
            model_selector,
            temperature_selector,
            self.divider,
            self.send_button,
        ]
        for widget in widgets:
            layout.addWidget(widget)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.chat_log.append_message("system", self.initial_prompt)
        self.prompt.setFocus()

    def load_state(self):
        self.loading_signal.connect(self.set_loading)
        self.initial_prompt = load_initial_prompt(self.settings)
        self.chatbot = Chatbot([{"role": "system", "content": self.initial_prompt}])
        self.opened_file = None
        self.is_loading = False

        geometry_key = "window/geometry"
        geometry = self.settings.value(geometry_key)
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(*self.default_window_geometry)

        temperature_key = "engines/temperature"
        saved_temperature = self.settings.value(temperature_key)
        if saved_temperature:
            self.temperature = saved_temperature
        else:
            self.temperature = 0.618
        self.settings.setValue(temperature_key, self.temperature)

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

    def set_to_save(self):
        self.setWindowTitle(
            f"{self.window_title} - {Utilities.path_strip(self.opened_file)}*"
            if self.opened_file
            else f"{self.window_title} - New Chat*"
        )

    def send_message(self):
        message = self.prompt.toPlainText()
        if message.strip() == "":
            self.prompt.setText("")
            self.prompt.setFocus()
            return
        self.chat_log.append_message("user", message)
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
        self.chat_log.append_message("assistant", response)
        self.is_loading = False
        self.loading_signal.emit(False)
        self.prompt.setFocus()

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
            self.chat_log.clear()
            self.chatbot = Chatbot(history)
            for message in history:
                self.chat_log.append_message(message["role"], message["content"])
            self.set_opened_file(loaded_file)

    def reload_history(self):
        if self.opened_file:
            history = Utilities.load_chat(self.opened_file)
            self.chat_log.clear()
            self.chatbot = Chatbot(history)
            for message in history:
                self.chat_log.append_message(message["role"], message["content"])

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
