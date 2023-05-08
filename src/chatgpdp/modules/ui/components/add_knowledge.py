from PyQt5.QtWidgets import QPushButton, QFileDialog, QWidget

from chatgpdp.modules.utils.config import PATHS


class Knowledge(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []

        self.btn = QPushButton("+ Add Knowledge")
        self.btn.clicked.connect(self.add_file)

    def add_file(self):
        new_file, _ = QFileDialog.getOpenFileName(self, "Open File", PATHS["base"], "PDF (*.pdf);;Text (*.txt)")
        if new_file:
            self.selected_files.append(new_file)
            self.btn.setText(new_file.split("/")[-1])
            self.btn.clicked.disconnect()
            self.btn.clicked.connect(self.remove_file)

    def remove_file(self):
        self.selected_files = []
        self.btn.setText("+ Add Knowledge")
        self.btn.clicked.disconnect()
        self.btn.clicked.connect(self.add_file)
