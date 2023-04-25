from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QDialogButtonBox,
)

from chatgpdp.modules.chat.bot import Chatbot
from chatgpdp.modules.utils.settings import Settings


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedWidth(600)
        layout = QVBoxLayout(self)

        options = [
            {
                "label": QLabel("OPENAI_API_KEY"),
                "value": QLineEdit(Settings().get_by_key("OPENAI_API_KEY")),
            }
        ]

        for option in options:
            layout.addWidget(option["label"])
            layout.addWidget(option["value"])

        layout.addWidget(QLabel(""))

        # Add the buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def write_env(self):
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                key = widget.parent().findChild(QLabel).text()
                value = widget.text()
                Settings().get().setValue(key, value)
                Settings().set_environ(key, value)
        Chatbot.reload_env(self)
