from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QComboBox, QLabel

from chatgpdp.modules.utils.config import engines, DEFAULT_ENGINE
from chatgpdp.modules.utils.settings import Settings
from chatgpdp.modules.utils.utilities import Utilities


class ModelSelector(QGroupBox):
    title = "Select a model:"

    def __init__(self):
        super().__init__()
        self.options = Utilities.get_engine_names(engines)
        self.settings = Settings()
        self.engine = self.settings.get_by_key("chat/engine") or engines[DEFAULT_ENGINE]["name"]
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.title))
        dropdown = QComboBox(self)
        dropdown.addItems(self.options)
        dropdown.setCurrentIndex(self.options.index(self.engine))
        dropdown.activated[str].connect(self.set_engine)
        layout.addWidget(dropdown)
        self.setLayout(layout)

    def set_engine(self, engine):
        self.engine = engine
        self.settings.get().setValue("chat/engine", engine)

    def get_engine(self):
        return self.engine
