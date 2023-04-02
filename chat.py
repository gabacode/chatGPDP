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


def setup():
    load_dotenv(override=True)
    openai.api_key = os.environ["OPENAI_API_KEY"]


def create_messages(prompt, history):
    messages = [{"role": "system", "content": initial_prompt}]
    for message in history:
        messages.append(message)
    history.append({"role": "user", "content": prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


def call_api(engine, messages, max_tokens, temperature):
    try:
        response = openai.ChatCompletion.create(
            model=engines[engine]["name"],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text = response["choices"][0]["message"]["content"].strip()
        return response_text
    except Exception as e:
        return "I'm sorry, we got an error:" + "\n" + str(e)


def chat(prompt, engine, temperature):
    setup()
    global history
    messages = create_messages(prompt, history)
    max_tokens = engines[engine]["max_tokens"] - len(prompt)
    chunks = [messages[i : i + max_tokens] for i in range(0, len(messages), max_tokens)]
    response_chunks = [call_api(engine, chunk, max_tokens, temperature) for chunk in chunks]
    response_text = "".join(response_chunks)
    log("\n" + "User: " + prompt + "\n" + "Assistant: " + response_text + "\n")
    history.append({"role": "system", "content": response_text})
    return response_text
