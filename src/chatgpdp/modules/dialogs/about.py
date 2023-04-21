from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QCursor
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from chatgpdp.resources import resources
from chatgpdp.modules.utils.utilities import Utilities


class AboutDialog(QDialog):
    metadata = Utilities.get_metadata()
    credits = [
        {"content": "<h3>chatGPDP</h3>"},
        {"content": "<p>Version {}</p>".format(metadata["Version"])},
        {"content": "<p>Made with love by<br><a href='https://github.com/gabacode'>Gabriele Arcangelo Scalici</a></p>"},
        {"content": "<p>Many thanks to <a href='https://openai.com/'>OpenAI</a>!</p>"},
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedWidth(420)

        layout = QVBoxLayout()

        icon_image = QLabel()
        icon_image.setPixmap(QPixmap(":/icons/chatgpdp.ico").scaled(96, 96))
        icon_image.setStyleSheet("border-radius: 50%;")
        icon_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_image)

        for credit in self.credits:
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
