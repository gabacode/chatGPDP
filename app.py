import os
import sys
from PyQt5 import QtWidgets, QtGui
from modules.ChatWindow import ChatWindow

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll

    myappid = "gabacode.chatGPDP.0.1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "icon.ico")))
    window = ChatWindow()
    window.setGeometry(100, 100, 800, 800)
    window.show()
    sys.exit(app.exec_())
