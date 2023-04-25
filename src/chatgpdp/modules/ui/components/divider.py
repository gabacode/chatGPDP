from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt


class Divider(QSplitter):
    def __init__(self, parent, top, bottom):
        super().__init__()
        self.parent = parent
        self.top = top
        self.bottom = bottom
        self.setup()

    def setup(self):
        self.setOrientation(Qt.Vertical)
        self.addWidget(self.top)
        self.addWidget(self.bottom)
        self.setSizes([300, 100])
        self.setCollapsible(0, False)
        self.setCollapsible(1, False)
