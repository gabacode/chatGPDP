from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")


def log(text):
    with open(f"chatlogs/{today}.txt", "a") as f:
        f.write(text)
    f.close()
