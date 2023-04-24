from typing import TYPE_CHECKING
from PyQt5.QtWidgets import QAction, QMenuBar
from chatgpdp.modules.utils.utilities import Utilities

if TYPE_CHECKING:
    from chatgpdp.modules.ui.chat_window import ChatWindow


class MenuBar(QMenuBar):
    generate_shortcut = Utilities.generate_shortcut
    shortcuts = {
        "New": generate_shortcut("N"),
        "Open": generate_shortcut("O"),
        "Reload": generate_shortcut("R"),
        "Save": generate_shortcut("S"),
        "SaveAs": generate_shortcut("Shift+S"),
        "Exit": generate_shortcut("Q"),
        "ChangePersonality": generate_shortcut("Shift+P"),
    }

    def __init__(self, chat_window: "ChatWindow") -> None:
        super().__init__()

        self.chat_window = chat_window

        self.menu_items = {
            "File": [
                ("New Chat", self.shortcuts["New"], self.chat_window.new_chat),
                ("Load Chat", self.shortcuts["Open"], self.chat_window.load_history),
                ("Save Chat", self.shortcuts["Save"], self.chat_window.save_history),
                ("Save Chat As...", self.shortcuts["SaveAs"], self.chat_window.save_history_as),
                ("Exit", self.shortcuts["Exit"], self.chat_window.close),
            ],
            "Edit": [
                ("Reload...", self.shortcuts["Reload"], self.chat_window.reload_history),
            ],
            "Options": [
                ("Set API Key...", None, self.chat_window.show_config_dialog),
                ("Change Personality...", self.shortcuts["ChangePersonality"], self.chat_window.change_personality),
            ],
            "Help": [
                ("About...", None, self.chat_window.show_about_dialog),
                ("Get API Key...", None, self.chat_window.get_api_key),
                ("View Source...", None, self.chat_window.go_to_github),
            ],
        }

        self.create_menu()

    def create_menu(self):
        for menu_title, items in self.menu_items.items():
            menu = self.addMenu(menu_title)
            for label, shortcut, function in items:
                action = QAction(label, self)
                if shortcut:
                    action.setShortcut(shortcut)
                action.triggered.connect(function)
                menu.addAction(action)
