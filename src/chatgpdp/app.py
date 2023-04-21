import sys
from chatgpdp.resources import resources

from chatgpdp.modules.utils.utilities import Utilities
from chatgpdp.modules.ui.chat_window import ChatWindow
from chatgpdp.styles.use_style import Style

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon


def app():
    metadata = Utilities.get_metadata()
    QApplication.setApplicationName(metadata["Formal-Name"])

    app = QApplication(sys.argv)
    try:
        app.setWindowIcon(QIcon(":/icons/chatgpdp.ico"))
        app.setStyleSheet(Style.get_style("main.qss"))
    except Exception as e:
        print(e)

    main_window = ChatWindow()
    main_window.setGeometry(100, 100, 800, 800)
    main_window.show()

    sys.exit(app.exec_())
