from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QFileDialog, QWidget
from PyQt5.QtCore import Qt

from chatgpdp.modules.utils.config import PATHS


class FileSelectDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.allowed_mime_types = ["text/plain", "application/pdf", "text/csv"]
        self.setup_dialog()

    def setup_dialog(self):
        self.setFileMode(QFileDialog.ExistingFile)
        self.setViewMode(QFileDialog.Detail)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setNameFilter("*.pdf *.csv *.txt *.php")
        #self.setMimeTypeFilters(self.allowed_mime_types)


class Knowledge(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_files = []
        self.setAcceptDrops(True)
        self.create_add_button()

    def create_add_button(self):
        self.btn = QPushButton("+ Add Knowledge")
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self.add_file)

    def add_file(self):
        dialog = FileSelectDialog(self, "Select File", PATHS["base"])
        dialog.exec_()

        selected_files = dialog.selectedFiles()
        if selected_files:
            self.selected_files = selected_files[:1]
            self.update_button_to_remove()

    def update_button_to_remove(self):
        self.btn.setStyleSheet("background-color: #4CAF50;")
        self.btn.setText(f"{self.selected_files[0].split('/')[-1]} - (Click to remove)")
        self.btn.clicked.disconnect()
        self.btn.clicked.connect(self.remove_file)

    def remove_file(self):
        self.selected_files = []
        self.update_button_to_add()

    def update_button_to_add(self):
        self.btn.setText("+ Add Knowledge")
        self.btn.clicked.disconnect()
        self.btn.clicked.connect(self.add_file)
        self.btn.setStyleSheet("")

    def dragEnterEvent(self, event):
        print(event)
        event.accept()
        return super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        print(event)
        return super().dragMoveEvent(event)

    def dropEvent(self, event):
        print(event)
        if len(self.selected_files) > 0:
            return
        self.selected_files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.update_button_to_remove()
        return super().dropEvent(event)
