from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTextEdit,
    QVBoxLayout,
)

from config import load_initial_prompt


class PersonalityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Personality")
        self.setFixedWidth(600)
        self.personality = load_initial_prompt()

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
        with open("initial_prompt.txt", "w") as f:
            f.write(self.personality)
        self.accept()

    def reject(self):
        self.done(QDialog.Rejected)
