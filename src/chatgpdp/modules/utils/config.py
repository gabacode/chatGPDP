from chatgpdp.modules.utils.utilities import Utilities

BASE_DIR = Utilities.get_project_root()
PATHS = {
    "base": BASE_DIR,
    "chatlogs": f"{BASE_DIR}/chatlogs",
    "env": f"{BASE_DIR}/.env",
}
PROMPTS = {"default": "You are a useful and intelligent assistant. Be creative and have fun!"}


def load_initial_prompt(settings):
    initial_prompt_key = "chat/initial_prompt"
    initial_prompt = settings.value(initial_prompt_key)
    if initial_prompt:
        return initial_prompt
    else:
        settings.setValue(initial_prompt_key, PROMPTS["default"])
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
