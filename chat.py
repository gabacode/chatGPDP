import os
import openai
from config import engines, initial_prompt
from utils import log
from datetime import datetime
from dotenv import load_dotenv


class Chatbot:
    def __init__(self):
        if not os.path.exists("chatlogs"):
            os.mkdir("chatlogs")
        else:
            log("\n" + "[Session started at " + str(datetime.now()) + "]\n")
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=")
        load_dotenv(override=True)
        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.is_thinking = False
        self.history = []

    def create_messages(self, prompt):
        messages = [{"role": "system", "content": initial_prompt}]
        for message in self.history:
            messages.append(message)
        self.history.append({"role": "user", "content": prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def call_api(self, engine, messages, max_tokens, temperature):
        self.is_thinking = True
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
        finally:
            self.is_thinking = False

    def chat(self, prompt, engine, temperature):
        messages = self.create_messages(prompt)
        max_tokens = engines[engine]["max_tokens"]
        chunks = [messages[i : i + max_tokens] for i in range(0, len(messages), max_tokens)]
        response_chunks = [self.call_api(engine, chunk, max_tokens, temperature) for chunk in chunks]
        response_text = "".join(response_chunks)
        log("\n" + "User: " + prompt + "\n" + "Assistant: " + response_text + "\n")
        self.history.append({"role": "assistant", "content": response_text})
        return response_text
