from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QComboBox, QLabel

from chatgpdp.modules.utils.config import engines
from chatgpdp.modules.utils.utilities import Utilities

class ModelSelector(QGroupBox):
    title = "Select a model"
    def __init__(self):
        super().__init__()
        self.options = Utilities.get_engine_names(engines)
        self.engine = self.engine, *_ = self.options
        self.initUI()

    def initUI(self):
        label = QLabel(f"{self.title}:")
        dropdown = QComboBox(self)
        dropdown.addItems(self.options)
        dropdown.setCurrentIndex(0)
        dropdown.activated[str].connect(self.set_engine)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(dropdown)
        self.setLayout(layout)

    def set_engine(self, text):
        self.engine = text

    def get_engine(self):
        return self.engine
