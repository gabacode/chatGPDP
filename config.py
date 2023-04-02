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

options = {
    "default_font": QFont("Arial", 12),
    "styles": {
        "box": "padding: 10px; background-color: #ffffff;",
    },
}
