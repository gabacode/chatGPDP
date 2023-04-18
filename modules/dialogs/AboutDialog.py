import os
from config import version
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from modules.Utilities import Utilities


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedWidth(420)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.icon = os.path.join(root_dir, "icon.ico")
        credits = [
            {"content": "<h3>chatGPDP</h3>"},
            {"content": "<p>Version {}</p>".format(version)},
            {"content": "<p>Made with love by<br><a href='https://github.com/gabacode'>Gabriele Arcangelo Scalici</a></p>"},
            {"content": "<p>Many thanks to <a href='https://openai.com/'>OpenAI</a>!</p>"},
        ]

        layout = QVBoxLayout()

        icon_image = QLabel()
        icon_image.setPixmap(QPixmap(self.icon).scaled(96, 96))
        icon_image.setStyleSheet("border-radius: 50%;")
        icon_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_image)

        for credit in credits:
            label = QLabel(credit["content"])
            label.setAlignment(Qt.AlignCenter)
            label.setOpenExternalLinks(True)
            label.linkActivated.connect(lambda url: Utilities.open_link(url))
            layout.addWidget(label)

        layout.addWidget(QLabel(""))

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Cheers!")
        ok_button.setCursor(QCursor(Qt.PointingHandCursor))
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
