import os
import openai
from config import engines
from utils import log
from datetime import datetime
from dotenv import load_dotenv

initial_prompt = "You are a useful and intelligent person."

if not os.path.exists("chatlogs"):
    os.mkdir("chatlogs")
else:
    log("\n" + "[Session started at " + str(datetime.now()) + "]\n")
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("OPENAI_API_KEY=")

history = []


def chat(prompt, engine, temperature):
    load_dotenv(override=True)
    openai.api_key = os.environ["OPENAI_API_KEY"]
    global history
    messages = [{"role": "system", "content": initial_prompt}]
    for message in history:
        messages.append(message)
    history.append({"role": "user", "content": prompt})
    messages.append({"role": "user", "content": prompt})
    try:
        response = openai.ChatCompletion.create(
            model=engines[engine]["name"],
            messages=messages,
            max_tokens=engines[engine]["max_tokens"] - len(prompt),
            temperature=temperature,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text = response["choices"][0]["message"]["content"].strip()
        log("\n" + "User: " + prompt + "\n" + "Assistant: " + response_text + "\n")
        history.append({"role": "system", "content": response_text})
        return response_text
    except Exception as e:
        return "I'm sorry, we got an error:" + "\n" + str(e)
