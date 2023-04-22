from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QSlider

class Temperature(QGroupBox):
    title = "Change temperature"
    def __init__(self, temperature):
        super().__init__()
        self.temperature = temperature
        self.label = QLabel()
        self.initUI()

    def initUI(self):
        self.set_label(self.temperature)
        slider = QSlider(
            Qt.Horizontal, minimum=0, maximum=1000, value=618, tickInterval=10, tickPosition=QSlider.TicksBelow
        )
        slider.valueChanged.connect(self.change_temperature)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(slider)
        self.setLayout(layout)

    def set_label(self, value):
        self.label.setText(f"{self.title}: {value}")

    def change_temperature(self, value):
        self.temperature = value / 1000.0
        self.set_label(self.temperature)

    def get_temperature(self):
        return self.temperature
