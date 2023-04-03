import os
import openai
from config import engines
from dotenv import load_dotenv


class Chatbot:
    def __init__(self, history):
        if not os.path.exists("chatlogs"):
            os.mkdir("chatlogs")
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=")
        self.reload_env()
        self.history = history

    def reload_env(self):
        load_dotenv(override=True)
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def create_messages(self, prompt):
        message = {"role": "user", "content": prompt}
        self.history.append(message)
        return self.history

    def call_api(self, engine, messages, max_tokens, temperature):
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

    def chat(self, prompt, engine, temperature):
        try:
            messages = self.create_messages(prompt)
            max_tokens = engines[engine]["max_tokens"]
            chunks = [messages[i : i + max_tokens] for i in range(0, len(messages), max_tokens)]
            response_chunks = [self.call_api(engine, chunk, max_tokens, temperature) for chunk in chunks]
            response_text = "".join(response_chunks)
            self.history.append({"role": "assistant", "content": response_text})
            return response_text
        except Exception as e:
            return "I'm sorry, we got an error:" + "\n" + str(e)

    def get_history(self):
        return self.history
