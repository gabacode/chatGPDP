import json
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices


class Utilities:
    def save_chat(file, history):
        if file.endswith(".json"):
            file = file.replace(".json", "")
        try:
            with open(f"{file}.json", "w") as f:
                json.dump(history, f, indent=2)
                return f.name
        except Exception as e:
            print(e)
            return False

    def load_chat(file):
        try:
            with open(file, "r") as f:
                history = json.load(f)
            return history
        except Exception as e:
            print(e)
            return []

    def get_engine_names(engines_dict):
        engine_names = []
        for engine in engines_dict.values():
            engine_names.append(engine["name"])
        return engine_names

    def generate_shortcut(name):
        if sys.platform == "darwin":
            return f"⌘{name}"
        else:
            return f"Ctrl+{name}"

    def get_name_from_mode(mode):
        return {"user": "You", "assistant": "Assistant"}.get(mode, "Personality")

    @staticmethod
    def open_link(url):
        QDesktopServices.openUrl(QUrl(url))

    def path_strip(path, keep_extension=False):
        formatted = path.split("/")[-1]
        if keep_extension:
            return formatted
        else:
            return formatted.split(".")[0]
