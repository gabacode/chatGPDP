from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QFrame,
    QSizePolicy,
    QVBoxLayout,
    QDialogButtonBox,
)

from chatgpdp.modules.chat.bot import Chatbot
from chatgpdp.modules.dialogs.components.color_picker import ColorPicker
from chatgpdp.modules.utils.settings import Settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedWidth(600)
        self.settings = Settings().get()
        layout = QVBoxLayout(self)

        # API key settings
        api_key_frame = QFrame()
        api_key_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        api_key_frame.setFrameShape(QFrame.StyledPanel)
        api_key_layout = QVBoxLayout(api_key_frame)
        self.api_key_label = QLabel("OPENAI_API_KEY")
        self.api_key_text = QLineEdit(self.settings.value("OPENAI_API_KEY"))
        api_key_layout.addWidget(self.api_key_label)
        api_key_layout.addWidget(self.api_key_text)

        # Colors settings
        colors_frame = QFrame()
        colors_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        colors_frame.setFrameShape(QFrame.StyledPanel)
        self.colors_layout = QVBoxLayout(colors_frame)
        color_scopes = ["system", "assistant", "user"]
        for scope in color_scopes:
            background = self.settings.value(f"colors/{scope}/background")
            foreground = self.settings.value(f"colors/{scope}/foreground")

            foreground_picker = ColorPicker(f"{scope}/foreground", "Text", foreground)
            background_picker = ColorPicker(f"{scope}/background", "Background", background)

            self.colors_layout.addWidget(QLabel(f"{scope.capitalize()} colors:"))
            self.colors_layout.addWidget(foreground_picker)
            self.colors_layout.addWidget(background_picker)

        layout.addWidget(api_key_frame)
        layout.addWidget(colors_frame)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def write_env(self):
        self.settings.setValue("OPENAI_API_KEY", self.api_key_text.text())
        self.settings.beginGroup("colors")
        for child in self.findChildren(ColorPicker):
            self.settings.setValue(child.scope, str(child.color).upper())
        self.settings.endGroup()
        Chatbot.reload_env(self)
