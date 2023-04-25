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
        label = QLabel("OPENAI_API_KEY")
        edit = QLineEdit(self.settings.value("OPENAI_API_KEY"))
        api_key_layout.addWidget(label)
        api_key_layout.addWidget(edit)

        # Colors settings
        colors_frame = QFrame()
        colors_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        colors_frame.setFrameShape(QFrame.StyledPanel)
        colors_layout = QVBoxLayout(colors_frame)
        color_scopes = ["system", "assistant", "user"]
        for scope in color_scopes:
            color = self.settings.value(f"colors/{scope}")
            background, foreground = color["background"], color["foreground"]

            foreground_picker = ColorPicker(f"colors/{scope}/foreground", "Text", foreground)
            background_picker = ColorPicker(f"colors/{scope}/background", "Background", background)

            colors_layout.addWidget(QLabel(f"{scope.capitalize()} colors:"))
            colors_layout.addWidget(foreground_picker)
            colors_layout.addWidget(background_picker)

        layout.addWidget(api_key_frame)
        layout.addWidget(colors_frame)

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
