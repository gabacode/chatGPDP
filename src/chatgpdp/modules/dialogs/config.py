from PySide2.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QDialogButtonBox,
)

from chatgpdp.modules.utils.config import PATHS
from chatgpdp.modules.chat.bot import Chatbot


class ConfigDialog(QDialog):
    env_path = PATHS["env"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedWidth(600)
        layout = QVBoxLayout(self)

        # Add the options
        options = self.read_env()
        for option in options:
            option_label = QLabel(option[0])
            option_edit = QLineEdit(option[1])
            layout.addWidget(option_label)
            layout.addWidget(option_edit)

        layout.addWidget(QLabel(""))

        # Add the buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def read_env(self):
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
        Chatbot.reload_env(self)
