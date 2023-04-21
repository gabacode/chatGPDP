from chatgpdp.modules.utils.utilities import Utilities

BASE_DIR = Utilities.get_project_root()
PATHS = {
    "base": BASE_DIR,
    "chatlogs": f"{BASE_DIR}/chatlogs",
    "env": f"{BASE_DIR}/.env",
    "initial_prompt": f"{BASE_DIR}/initial_prompt.txt",
}
PROMPTS = {"default": "You are a useful and intelligent assistant. Be creative and have fun!"}


def load_initial_prompt(retries=3):
    try:
        with open(PATHS["initial_prompt"], "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        if retries > 0:
            with open(PATHS["initial_prompt"], "w") as f:
                f.write(PROMPTS["default"])
            return load_initial_prompt(retries - 1)
        return PROMPTS["default"]
    except Exception as e:
        print(e)
        return PROMPTS["default"]


colors = {
    "user": {
        "background": "#F0F0F0",
        "foreground": "#000000",
    },
    "assistant": {
        "background": "#F0F0F0",
        "foreground": "#000000",
    },
    "system": {
        "background": "#F0F0F0",
        "foreground": "#000000",
    },
}

engines = {
    "gpt-3.5-turbo": {
        "name": "gpt-3.5-turbo",
        "max_tokens": 2048,
    },
}

generate_shortcut = Utilities.generate_shortcut
shortcuts = {
    "New": generate_shortcut("N"),
    "Open": generate_shortcut("O"),
    "Reload": generate_shortcut("R"),
    "Save": generate_shortcut("S"),
    "SaveAs": generate_shortcut("Shift+S"),
    "Exit": generate_shortcut("Q"),
    "ChangePersonality": generate_shortcut("Shift+P"),
}
