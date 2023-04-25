import os
import sys
import json
from pathlib import Path

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    import importlib_metadata


class Utilities:
    """
    A collection of utility functions.

    Methods:
        - get_project_root() -> str
        - save_chat(file: str, history: list) -> str
        - load_chat(file: str) -> list
        - get_engine_names(engines_dict: dict) -> list
        - generate_shortcut(name: str) -> str
        - get_name_from_mode(mode: str) -> str
        - open_link(url: str) -> None
        - path_strip(path: str, keep_extension: bool = False) -> str
        - get_metadata() -> dict
    """

    @staticmethod
    def get_project_root() -> str:
        """
        Returns the root directory of the current Python project.
        """
        main_file = Path(os.path.abspath(sys.argv[0]))
        root_folder = main_file.parents[2]
        return str(root_folder)

    @staticmethod
    def save_chat(file: str, history: list) -> str:
        """
        Saves the chat history to a JSON file.
        """
        if file.endswith(".json"):
            file = file.replace(".json", "")
        try:
            with open(f"{file}.json", "w") as f:
                json.dump(history, f, indent=2)
                return f.name
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def load_chat(file: str) -> list:
        """
        Loads the chat history from a JSON file.
        """
        try:
            with open(file, "r") as f:
                history = json.load(f)
            return history
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_engine_names(engines_dict: dict) -> list:
        """
        Returns a list of engine names from a dictionary of engines.
        """
        engine_names = []
        for engine in engines_dict.values():
            engine_names.append(engine["name"])
        return engine_names

    @staticmethod
    def generate_shortcut(name: str) -> str:
        """
        Returns a platform-specific shortcut string.
        """
        if sys.platform == "darwin":
            return f"⌘{name}"
        else:
            return f"Ctrl+{name}"

    @staticmethod
    def get_name_from_mode(mode):
        """
        Returns a name for a chat bubble based on the message's sender.
        """
        return {"user": "You", "assistant": "Assistant"}.get(mode, "System")

    @staticmethod
    def open_link(url):
        """
        Opens a link in the user's default browser.
        """
        QDesktopServices.openUrl(QUrl(url))

    @staticmethod
    def path_strip(path, keep_extension=False):
        """
        Returns the filename from a path.
        """
        formatted = path.split("/")[-1]
        if keep_extension:
            return formatted
        else:
            return formatted.split(".")[0]

    @staticmethod
    def get_metadata():
        """
        Returns the metadata for the current Python project.
        """
        app_module = sys.modules["__main__"].__package__
        metadata = importlib_metadata.metadata(app_module)
        return metadata
