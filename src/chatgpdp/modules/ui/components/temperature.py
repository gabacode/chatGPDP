from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QSlider

class Temperature(QGroupBox):
    title = "Select a temperature"
    def __init__(self, temperature):
        super().__init__()
        self.temperature = temperature
        self.temperature_label = QLabel()
        self.initUI()

    def initUI(self):
        self.set_label(self.temperature)
        temperature_slider = QSlider(
            Qt.Horizontal, minimum=0, maximum=1000, value=618, tickInterval=10, tickPosition=QSlider.TicksBelow
        )
        temperature_slider.valueChanged.connect(self.change_temperature)

        temperature_layout = QVBoxLayout()
        temperature_layout.addWidget(self.temperature_label)
        temperature_layout.addWidget(temperature_slider)
        self.setLayout(temperature_layout)

    def set_label(self, value):
        self.temperature_label.setText(f"{self.title}: {value}")

    def change_temperature(self, value):
        self.temperature = value / 1000.0
        self.set_label(self.temperature)

    def get_temperature(self):
        return self.temperature
