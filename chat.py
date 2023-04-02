import os
import openai
from config import engines
from utils import log
from datetime import datetime
from dotenv import load_dotenv

"""
Put your Open AI API key in a .env file
"""

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
initial_prompt = "You are the Italian Garante. You are investigating the Italian government's response to the chatGPT privacy policy. You are looking for evidence of corruption. You are looking for evidence of incompetence. You are looking for evidence of negligence. You are looking for evidence of malfeasance. You are looking for evidence of misfeasance. You are looking for evidence of nonfeasance. You are looking for evidence of abuse of power. You are looking for evidence of abuse of authority. You are looking for evidence of abuse of discretion. You are looking for evidence of abuse of process. You are looking for evidence of abuse of trust. You are looking for evidence of abuse of office. You are looking for evidence of abuse of position. You are looking for evidence of abuse"
history = []

if not os.path.exists("chatlogs"):
    os.mkdir("chatlogs")
else:
    log("\n" + "[Session started at " + str(datetime.now()) + "]\n")


def chat(prompt, engine, temperature):
    global history
    messages = [{"role": "system", "content": initial_prompt}]
    for message in history:
        messages.append(message)
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
    except openai.InvalidRequestError as e:
        print(e)
