import os

from modules.Utilities import Utilities

version = "0.2.2"

generate_shortcut = Utilities.generate_shortcut

default_prompt = "You are a useful and intelligent assistant. Be creative and have fun!"


def load_initial_prompt(retries=3):
    try:
        with open("initial_prompt.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        if retries > 0:
            with open("initial_prompt.txt", "w") as f:
                f.write(default_prompt)
            return load_initial_prompt(retries - 1)
        return default_prompt
    except Exception as e:
        print(e)
        return default_prompt


colors = {
    "user": "#2ECC71",
    "assistant": "#007AFF",
    "system": "#bbb",
}

engines = {
    "gpt-3.5-turbo": {
        "name": "gpt-3.5-turbo",
        "max_tokens": 2048,
    },
}

chatlogs_directory = "chatlogs"

shortcuts = {
    "New": generate_shortcut("N"),
    "Open": generate_shortcut("O"),
    "Save": generate_shortcut("S"),
    "SaveAs": generate_shortcut("Shift+S"),
    "Exit": generate_shortcut("Q"),
}
