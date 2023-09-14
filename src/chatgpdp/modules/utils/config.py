from PyQt5.QtCore import QStandardPaths

BASE_DIR = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
PATHS = {
    "base": BASE_DIR,
    "chatlogs": f"{BASE_DIR}/chatGPDP/chatlogs",
    "screenshots": f"{BASE_DIR}/chatGPDP/screenshots",
    "embeddings": f"{BASE_DIR}/chatGPDP/embeddings",
    "models": f"{BASE_DIR}/chatGPDP/models",
}
DEFAULT_ENGINE = "gpt-3.5-turbo"
PROMPTS = {"default": "You are a useful and intelligent assistant. Be creative and have fun!"}

engines_list = {
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
    "ggml-gpt4all-j-v1.3-groovy.bin": {
        "name": "ggml-gpt4all-j-v1.3-groovy.bin",
        "max_tokens": 2048,
    },
    "wizardLM-13B-Uncensored.ggmlv3.q4_0.bin": {
        "name": "wizardLM-13B-Uncensored.ggmlv3.q4_0.bin",
        "max_tokens": 2048,
    },
    "nous-hermes-13b.ggmlv3.q4_0.bin": {
        "name": "nous-hermes-13b.ggmlv3.q4_0.bin",
        "max_tokens": 2048,
    },
    "llama-2-7b-chat.ggmlv3.q2_K.bin": {
        "name": "llama-2-7b-chat.ggmlv3.q2_K.bin",
        "max_tokens": 2048,
    },
    "ggml-replit-code-v1-3b.bin": {
        "name": "ggml-replit-code-v1-3b.bin",
        "max_tokens": 2048,
    },
}

engines = {k: v for k, v in sorted(engines_list.items())}

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
