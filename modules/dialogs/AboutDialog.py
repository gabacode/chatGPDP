import os
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedWidth(420)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.icon = os.path.join(root_dir, "icon.ico")
        credits = [
            {"content": "<h3>chatGPDP</h3>"},
            {"content": "<p>Version 0.1</p>"},
            {"content": "<p>Made with love by<br><a href='https://github.com/gabacode'>Gabriele Arcangelo Scalici</a></p>"},
            {"content": "<p>Many thanks to <a href='https://openai.com/'>OpenAI</a>!</p>"},
        ]

        def open_link(self, url):
            QDesktopServices.openUrl(QUrl(url))

        layout = QVBoxLayout()

        icon_image = QLabel()
        icon_image.setPixmap(QPixmap(self.icon).scaled(128, 128))
        icon_image.setStyleSheet("border-radius: 50%;")
        icon_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_image)

        for credit in credits:
            label = QLabel(credit["content"])
            label.setAlignment(Qt.AlignCenter)
            label.setOpenExternalLinks(True)
            label.linkActivated.connect(lambda url: open_link(self, url))
            layout.addWidget(label)

        layout.addWidget(QLabel(""))

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Cheers!")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

