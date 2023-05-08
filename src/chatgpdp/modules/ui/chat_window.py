import os
import sys
from datetime import datetime

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
from PyQt5.QtGui import QPixmap

from chatgpdp.modules import ModelSelector, Temperature, Chatbot
from chatgpdp.modules.dialogs import AboutDialog, SettingsDialog, PersonalityDialog
from chatgpdp.modules.ui.components import MenuBar, ChatBox, Divider, PromptBox, SendButton
from chatgpdp.modules.ui.components.add_knowledge import Knowledge
from chatgpdp.modules.utils.config import PATHS
from chatgpdp.modules.utils import Settings, Utilities
from chatgpdp.modules.threads.chat import ChatThread


class ChatWindow(QMainWindow):
    loading_signal = pyqtSignal(bool)
    settings = Settings().get()
    default_window_geometry = (100, 100, 800, 800)

    def __init__(self, metadata):
        super().__init__()
        self.metadata = metadata
        self.window_title = f"{metadata['Formal-Name']} v{metadata['Version']}"

        self.load_state()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.window_title)
        self.setMenuBar(MenuBar(self))

        self.knowledge = Knowledge()

        self.model_selector = ModelSelector()
        self.engine = self.model_selector.get_engine()
        self.model_selector.set_engine = self.update_engine
        self.temperature_selector = Temperature(self.temperature)

        self.chat_box = ChatBox(self)
        self.prompt_box = PromptBox(self)
        self.divider = Divider(self, self.chat_box, self.prompt_box)

        self.send_button = SendButton(on_click=self.send_message)

        layout = QVBoxLayout()
        widgets = [
            self.model_selector,
            self.temperature_selector,
            self.knowledge.btn,
            self.divider,
            self.send_button,
        ]
        for widget in widgets:
            layout.addWidget(widget)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.chat_box.append_message("system", self.initial_prompt)
        self.prompt_box.setFocus()

    def update_engine(self, engine):
        self.engine = engine

    def load_state(self):
        self.loading_signal.connect(self.set_loading)
        self.initial_prompt = self.settings.value("chat/initial_prompt")
        self.temperature = self.settings.value("chat/temperature")

        self.chatbot = Chatbot([{"role": "system", "content": self.initial_prompt}])
        self.opened_file = None
        self.is_loading = False

        geometry = self.settings.value("window/geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(*self.default_window_geometry)

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
        message = self.prompt_box.toPlainText()
        if message.strip() == "":
            self.prompt_box.setText("")
            self.prompt_box.setFocus()
            return
        self.chat_box.append_message("user", message)
        self.set_to_save()
        self.prompt_box.clear()

        self.is_loading = True
        self.loading_signal.emit(True)

        if hasattr(self, "chat_thread") and self.chat_thread.isRunning():
            self.chat_thread.terminate()
            self.chat_thread.wait()

        engine = self.model_selector.get_engine()
        temperature = self.temperature_selector.get_temperature()

        self.chat_thread = ChatThread(self.chatbot, message, engine, temperature, self.knowledge.selected_files)
        self.chat_thread.response_signal.connect(self.handle_response)
        self.chat_thread.start()

    def handle_response(self, response):
        self.chat_box.append_message("assistant", response)
        self.is_loading = False
        self.loading_signal.emit(False)
        self.prompt_box.setFocus()

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def show_settings(self):
        config_dialog = SettingsDialog(self)
        if config_dialog.exec_() == QDialog.Accepted:
            config_dialog.save_settings()
        else:
            config_dialog.close()

    def change_personality(self):
        personality_dialog = PersonalityDialog(self)
        if personality_dialog.exec_() == QDialog.Accepted:
            self.close()
            self.new_chat()

    def new_chat(self):
        self.new_window = ChatWindow(self.metadata)
        self.new_window.setGeometry(*self.default_window_geometry)
        self.new_window.show()

    def restart_chat(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def set_opened_file(self, file_name):
        self.opened_file = file_name
        self.setWindowTitle(f"{self.window_title} - {Utilities.path_strip(file_name)}")

    def save_history(self):
        if self.opened_file:
            Utilities.save_chat(self.opened_file, self.chatbot.history)
            self.set_opened_file(self.opened_file)
        else:
            self.save_history_as()

    def load_history(self, loaded_file=None):
        if not loaded_file:
            loaded_file, _ = QFileDialog.getOpenFileName(self, "Open File", PATHS["chatlogs"], "JSON Files (*.json)")
            if not loaded_file:
                return
        history = Utilities.load_chat(loaded_file)
        self.chat_box.clear()
        self.chatbot = Chatbot(history)
        for message in history:
            self.chat_box.append_message(message["role"], message["content"])
        self.set_opened_file(loaded_file)

    def save_history_as(self):
        new_file, _ = QFileDialog.getSaveFileName(self, "Save File", PATHS["chatlogs"], "JSON Files (*.json)")
        if new_file:
            Utilities.save_chat(new_file, self.chatbot.history)
            self.set_opened_file(new_file)

    def reload_history(self):
        self.load_history(loaded_file=self.opened_file)

    def take_screen_shot(self):
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        widget = self.chat_box.widget()
        screenshot = widget.grab()
        pix = QPixmap(screenshot)
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", f"chatGPDP-{date_string}.png", "PNG Files (*.png)"
        )
        if file_name:
            pix.save(file_name, "PNG")

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
