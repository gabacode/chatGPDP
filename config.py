from PyQt5.QtGui import QFont

initial_prompt = "You are a useful and intelligent person. You're a Python master!"

colors = {
    "user": "#4CD964",
    "assistant": "#007AFF",
    "system": "#d0d0d0",
}

engines = {
    "gpt-3.5-turbo-0301": {
        "name": "gpt-3.5-turbo-0301",
        "max_tokens": 2048,
    },
    "davinci": {
        "name": "text-davinci-003",
        "max_tokens": 4097,
    },
    "curie": {"name": "text-curie-001", "max_tokens": 2048},
    "babbage": {"name": "text-babbage-001", "max_tokens": 2048},
    "ada": {"name": "text-ada-001", "max_tokens": 2048},
}

styles = {
    "box": "padding: 10px; background-color: #ffffff;",
    "scroll_bar_vertical": """
            QScrollBar:vertical {
                border: none;
                background-color: #F5F5F5;
                width: 14px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #B5B5B5;
                min-height: 50px;
                border: none;
                subcontrol-position: center;
            }

            QScrollBar::add-line:vertical {
                border: none;
                background-color: #F5F5F5;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                border: none;
                background-color: #F5F5F5;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """,
}

options = {
    "default_font": QFont("Arial", 12),
    "styles": styles,
}
