import sys
from PyQt5.QtWidgets import (
    QApplication,
)
from widgets.ChatWindow import ChatWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.setGeometry(100, 100, 800, 800)
    window.show()
    sys.exit(app.exec_())
