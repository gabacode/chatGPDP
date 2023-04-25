from PyQt5.QtWidgets import QFrame, QColorDialog, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class ColorPicker(QFrame):
    def __init__(self, scope, title, color):
        super().__init__()

        self.scope = scope
        self.title = title
        self.color = color

        layout = QHBoxLayout(self)
        label = QLabel(self.title)

        self.button = QPushButton()
        self.button.setFixedSize(20, 20)
        self.button.setCursor(Qt.PointingHandCursor)
        self.set_color()
        self.button.clicked.connect(self.pick_color)

        layout.addWidget(label)
        layout.addWidget(self.button)

    def pick_color(self):
        color = QColorDialog.getColor(initial=QColor(self.color))
        if color.isValid():
            self.color = color.name()
            self.set_color()

    def set_color(self):
        self.button.setStyleSheet(f"background-color: {self.color}; border: 1px solid black; border-radius: none;")
