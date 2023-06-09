from PyQt5.QtCore import QThread, pyqtSignal


class ChatThread(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, chatbot, message, engine, temperature):
        super().__init__()
        self.chatbot = chatbot
        self.message = message
        self.engine = engine
        self.temperature = temperature

    def run(self):
        response = self.chatbot.chat(self.message, self.engine, self.temperature)
        self.response_signal.emit(response)
