import os
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QDialogButtonBox,
)


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.env_path = ".env"
        self.setWindowTitle("Configuration")
        self.setFixedWidth(600)
        layout = QVBoxLayout(self)

        # Add the options
        options = self.read_env()
        for option in options:
            option_label = QLabel(option[0])
            option_edit = QLineEdit(option[1])
            layout.addWidget(option_label)
            layout.addWidget(option_edit)

        # Add the buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def init_env(self):
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=")

    def read_env(self):
        self.init_env()
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
