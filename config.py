import os

from modules.Utilities import Utilities

generate_shortcut = Utilities.generate_shortcut

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


shortcuts = {
    "New": generate_shortcut("N"),
    "Open": generate_shortcut("O"),
    "Save": generate_shortcut("S"),
    "SaveAs": generate_shortcut("Shift+S"),  # TODO: implement
    "Exit": generate_shortcut("Q"),
}
