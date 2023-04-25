from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTextEdit,
    QVBoxLayout,
)

from chatgpdp.modules.utils.settings import Settings


class PersonalityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Personality")
        self.setFixedWidth(600)
        self.settings = Settings()
        self.personality = self.settings.get_by_key("chat/initial_prompt")

        self.text_area = QTextEdit()

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_file_and_close)
        button_box.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(self.text_area)
        vbox.addWidget(button_box)
        self.setLayout(vbox)

        self.text_area.setText(self.personality)

    def save_file_and_close(self):
        self.personality = self.text_area.toPlainText()
        self.settings.get().setValue("chat/initial_prompt", self.personality)
        self.accept()

    def reject(self):
        self.done(QDialog.Rejected)
