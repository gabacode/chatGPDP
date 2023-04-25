from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QSlider

from chatgpdp.modules.utils.settings import Settings


class Temperature(QGroupBox):
    title = "Change temperature"

    def __init__(self, temperature):
        super().__init__()
        self.settings = Settings().get()
        self.temperature = temperature
        self.label = QLabel()
        self.initUI()

    def initUI(self):
        self.set_label(self.temperature)
        number = int(float(self.temperature) * 1000)
        slider = QSlider(
            Qt.Horizontal, minimum=0, maximum=1000, value=number, tickInterval=10, tickPosition=QSlider.TicksBelow
        )
        slider.valueChanged.connect(self.set_temperature)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(slider)
        self.setLayout(layout)

    def set_label(self, value):
        self.label.setText(f"{self.title}: {value}")

    def set_temperature(self, value):
        self.temperature = value / 1000.0
        self.set_label(self.temperature)
        self.settings.setValue("chat/temperature", self.temperature)

    def get_temperature(self):
        return self.temperature
