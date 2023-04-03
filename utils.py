from datetime import datetime
import json


def log(text):
    today = datetime.now()
    with open(f"chatlogs/{today}.txt", "a") as f:
        f.write(text)
    f.close()


def save_history(history):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(f"chatlogs/{today}.json", "w") as f:
        json.dump(history, f)
    f.close()


def load_history(file):
    try:
        with open(file, "r") as f:
            history = json.load(f)
        f.close()
        return history
    except:
        return []
