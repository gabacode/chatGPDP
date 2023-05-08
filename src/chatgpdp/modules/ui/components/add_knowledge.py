from PyQt5.QtWidgets import QCheckBox, QFileDialog, QWidget

from chatgpdp.modules.utils.config import PATHS


class Knowledge(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.with_documents = False

        self.cb = QCheckBox("With Documents")
        self.cb.stateChanged.connect(self.change_box)

    def change_box(self):
        if self.cb.isChecked():
            self.with_documents = True
            self.add_file()
        else:
            self.with_documents = False

    def add_file(self):
        new_file, _ = QFileDialog.getOpenFileName(
            self, "Open File", PATHS["base"], "PDF (*.pdf);;Text (*.txt)"
        )
        if new_file:
            self.selected_file = new_file
        else:
            self.selected_file = None
            self.cb.setChecked(False)
