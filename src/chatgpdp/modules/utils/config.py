from PyQt5.QtCore import QStandardPaths

BASE_DIR = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
PATHS = {
    "base": BASE_DIR,
    "chatlogs": f"{BASE_DIR}/chatGPDP/chatlogs",
    "screenshots": f"{BASE_DIR}/chatGPDP/screenshots",
    "embeddings": f"{BASE_DIR}/chatGPDP/embeddings",
}
DEFAULT_ENGINE = "gpt-3.5-turbo"
PROMPTS = {"default": "You are a useful and intelligent assistant. Be creative and have fun!"}

engines = {
    "gpt-3.5-turbo": {
        "name": "gpt-3.5-turbo",
        "max_tokens": 2048,
    },
    "gpt-3.5-turbo-0301": {
        "name": "gpt-3.5-turbo-0301",
        "max_tokens": 4096,
    },
    "gpt-3.5-turbo-0613": {
        "name": "gpt-3.5-turbo-0613",
        "max_tokens": 8192,
    },
    "gpt-3.5-turbo-16k": {
        "name": "gpt-3.5-turbo-16k",
        "max_tokens": 16384,
    },
    "gpt-4": {
        "name": "gpt-4",
        "max_tokens": 8192,
    },
    "gpt-4-32k": {
        "name": "gpt-4-32k",
        "max_tokens": 32768,
    },
    "gpt-4-0314": {
        "name": "gpt-4-0314",
        "max_tokens": 8192,
    },
}

DEFAULT_SETTINGS = {
    "OPENAI_API_KEY": "",
    "chat": {
        "engine": engines[DEFAULT_ENGINE]["name"],
        "initial_prompt": PROMPTS["default"],
        "max_tokens": engines[DEFAULT_ENGINE]["max_tokens"],
        "temperature": 0.618,
    },
    "colors": {
        "user": {
            "label": "#000000",
            "background": "#F0F0F0",
            "text": "#000000",
        },
        "assistant": {
            "label": "#000000",
            "background": "#F0F0F0",
            "text": "#000000",
        },
        "system": {
            "label": "#000000",
            "background": "#F0F0F0",
            "text": "#000000",
        },
    },
    "window": {
        "geometry": "",
    },
}
