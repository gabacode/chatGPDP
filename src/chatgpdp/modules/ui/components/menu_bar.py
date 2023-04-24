from PyQt5.QtWidgets import QAction, QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, chat_window, shortcuts):
        super().__init__()

        self.chat_window = chat_window

        self.menu_items = {
            "File": [
                ("New Chat", shortcuts["New"], self.chat_window.new_chat),
                ("Load Chat", shortcuts["Open"], self.chat_window.load_history),
                ("Save Chat", shortcuts["Save"], self.chat_window.save_history),
                ("Save Chat As...", shortcuts["SaveAs"], self.chat_window.save_history_as),
                ("Exit", shortcuts["Exit"], self.chat_window.close),
            ],
            "Edit": [
                ("Reload...", shortcuts["Reload"], self.chat_window.reload_history),
            ],
            "Options": [
                ("Set API Key...", None, self.chat_window.show_config_dialog),
                ("Change Personality...", shortcuts["ChangePersonality"], self.chat_window.change_personality),
            ],
            "Help": [
                ("About...", None, self.chat_window.show_about_dialog),
                ("Get API Key...", None, self.chat_window.get_api_key),
                ("View Source...", None, self.chat_window.go_to_github),
            ],
        }

        self.setup()

    def setup(self):
        for menu_title, items in self.menu_items.items():
            menu = self.addMenu(menu_title)
            for label, shortcut, function in items:
                action = QAction(label, self)
                if shortcut:
                    action.setShortcut(shortcut)
                action.triggered.connect(function)
                menu.addAction(action)
