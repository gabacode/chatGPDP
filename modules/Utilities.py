from datetime import datetime
import json


class Utilities:
    def __init__(self):
        pass

    def log(text):
        today = datetime.now()
        with open(f"chatlogs/{today}.txt", "a") as f:
            f.write(text)
        f.close()

    def save_chat(file, history):
        if file.endswith(".json"):
            file = file.replace(".json", "")
        with open(f"{file}.json", "w") as f:
            json.dump(history, f)
        f.close()

    def load_chat(file):
        try:
            with open(file, "r") as f:
                history = json.load(f)
            f.close()
            return history
        except:
            return []

    def get_engine_names(engines_dict):
        engine_names = []
        for engine in engines_dict.values():
            engine_names.append(engine["name"])
        return engine_names
