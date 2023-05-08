from PyQt5.QtCore import QThread, pyqtSignal


class ChatThread(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, chatbot, message, engine, temperature, selected_files):
        super().__init__()
        self.chatbot = chatbot
        self.message = message
        self.engine = engine
        self.temperature = temperature
        self.files = selected_files

    def run(self):
        # TODO: Add support for multiple files
        if len(self.files) > 0:
            response = self.chatbot.qa(self.message, self.engine, self.temperature, self.files[0])
        else:
            response = self.chatbot.chat(self.message, self.engine, self.temperature)

        self.response_signal.emit(response)
