from PyQt5.QtCore import QStandardPaths

BASE_DIR = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
PATHS = {
    "base": BASE_DIR,
    "chatlogs": f"{BASE_DIR}/chatGPDP/chatlogs",
    "screenshots": f"{BASE_DIR}/chatGPDP/screenshots",
    "embeddings": f"{BASE_DIR}/chatGPDP/embeddings",
}
PROMPTS = {"default": "You are a useful and intelligent assistant. Be creative and have fun!"}


DEFAULT_SETTINGS = {
    "OPENAI_API_KEY": "",
    "chat": {
        "initial_prompt": PROMPTS["default"],
        "max_tokens": 2048,
        "temperature": 0.618,
    },
    "colors": {
        "user": {
            "label": "#000000",
            "background": "#F0F0F0",
            "foreground": "#000000",
        },
        "assistant": {
            "label": "#000000",
            "background": "#F0F0F0",
            "foreground": "#000000",
        },
        "system": {
            "label": "#000000",
            "background": "#F0F0F0",
            "foreground": "#000000",
        },
    },
    "window": {
        "geometry": "",
    },
}


engines = {
    "gpt-3.5-turbo": {
        "name": "gpt-3.5-turbo",
        "max_tokens": 2048,
    },
    "gpt-3.5-turbo-0301": {
        "name": "gpt-3.5-turbo-0301",
        "max_tokens": 4096,
    },
}
