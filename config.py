import os

if "initial_prompt.txt" not in os.listdir():
    with open("initial_prompt.txt", "w") as f:
        f.write("Hello, I am a chatbot. How can I help you?")

version = 0.2

initial_prompt = open("initial_prompt.txt", "r").read().strip()

colors = {
    "user": "#4CD964",
    "assistant": "#007AFF",
    "system": "#bbb",
}

engines = {
    "gpt-3.5-turbo": {
        "name": "gpt-3.5-turbo",
        "max_tokens": 2048,
    },
}

styles = {
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
    "styles": styles,
}
