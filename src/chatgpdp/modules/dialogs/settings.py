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
        colors_frame_title = QLabel("Colors:")
        colors_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        colors_frame.setFrameShape(QFrame.StyledPanel)
        self.colors_layout = QVBoxLayout(colors_frame)
        self.colors_layout.addWidget(colors_frame_title)
        color_scopes = ["system", "assistant", "user"]
        for scope in color_scopes:
            inner_frame = QFrame()

            divider = QFrame()
            divider.setFrameShape(QFrame.HLine)
            divider.setFrameShadow(QFrame.Sunken)
            self.colors_layout.addWidget(divider)

            background = self.settings.value(f"colors/{scope}/background")
            label = self.settings.value(f"colors/{scope}/label")
            foreground = self.settings.value(f"colors/{scope}/foreground")

            label_picker = ColorPicker(f"{scope}/label", "Label:", label)
            background_picker = ColorPicker(f"{scope}/background", "Background:", background)
            foreground_picker = ColorPicker(f"{scope}/foreground", "Message:", foreground)

            self.colors_layout.addWidget(QLabel(f"{scope.capitalize()}:"))
            inner_layout = QVBoxLayout(inner_frame)
            inner_layout.addWidget(label_picker)
            inner_layout.addWidget(foreground_picker)
            inner_layout.addWidget(background_picker)

            self.colors_layout.addWidget(inner_frame)

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
