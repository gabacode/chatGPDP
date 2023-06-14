from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QWidget,
    QDialogButtonBox,
)

from PyQt5.QtCore import Qt

from chatgpdp.modules.chat.bot import Chatbot
from chatgpdp.modules.dialogs.components.color_picker import ColorPicker
from chatgpdp.modules.utils.settings import Settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(600)
        self.settings = Settings().get()

        self.api_settings = ApiSettings(self.settings)
        colors_settings = ColorSetting(self.settings)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        for button in button_box.buttons():
            button.setCursor(Qt.PointingHandCursor)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area_content = QWidget(scroll_area)
        scroll_area.setWidget(scroll_area_content)

        scroll_area_layout = QVBoxLayout(scroll_area_content)
        scroll_area_layout.addWidget(self.api_settings)
        scroll_area_layout.addWidget(colors_settings)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addStretch()
        button_layout.addWidget(button_box)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_widget)

    def save_settings(self):
        self.settings.setValue("OPENAI_API_KEY", self.api_settings.get_value())
        self.settings.beginGroup("colors")
        for child in self.findChildren(ColorPicker):
            self.settings.setValue(child.scope, str(child.color).upper())
        self.settings.endGroup()
        Chatbot.reload_env(self)


class ApiSettings(QGroupBox):
    def __init__(self, settings):
        super().__init__("OpenAI API Key")
        self.settings = settings
        layout = QVBoxLayout(self)
        self.value = QLineEdit(self.settings.value("OPENAI_API_KEY"))
        layout.addWidget(self.value)

    def get_value(self):
        return self.value.text()


class ColorSetting(QGroupBox):
    def __init__(self, settings):
        super().__init__("Colors")
        self.settings = settings
        layout = QVBoxLayout(self)
        for scope in ["system", "assistant", "user"]:
            group_box = QGroupBox(scope.capitalize())
            group_box_layout = QVBoxLayout(group_box)
            for color_type in ["label", "text", "background"]:
                color_value = self.settings.value(f"colors/{scope}/{color_type}")
                color_picker = ColorPicker(f"{scope}/{color_type}", f"{color_type.capitalize()}:", color_value)
                group_box_layout.addWidget(color_picker)
            layout.addWidget(group_box)
