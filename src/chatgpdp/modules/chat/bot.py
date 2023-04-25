import os
import openai
from dotenv import load_dotenv

from chatgpdp.modules.utils.config import PATHS, engines

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory

from chatgpdp.modules.utils.settings import Settings


class Chatbot:
    chatlogs_directory = PATHS["chatlogs"]
    screenshot_directory = PATHS["screenshots"]
    settings = Settings().get()

    def __init__(self, history):
        self.env_init()
        self.history = history
        self.memory = ConversationBufferMemory(return_messages=True)

    def env_init(self):
        if not os.path.exists(self.chatlogs_directory):
            os.mkdir(self.chatlogs_directory)
        if not os.path.exists(self.screenshot_directory):
            os.mkdir(self.screenshot_directory)
        self.reload_env()

    def reload_env(self):
        load_dotenv(override=True)
        key = Settings().get_by_key("OPENAI_API_KEY")
        openai.api_key = key

    def create_messages(self, prompt):
        self.add_to_history({"role": "user", "content": prompt})
        return self.history

    def get_initial_prompt(self):
        for message in self.history:
            if message["role"] == "system":
                return message["content"]

    def load_memory(self, history):
        messages = []
        for message in history:
            if message["role"] == "user":
                messages.append(HumanMessage(content=message["content"], additional_kwargs={}))
            elif message["role"] == "assistant":
                messages.append(AIMessage(content=message["content"], additional_kwargs={}))
        chat_memory = ChatMessageHistory(messages=messages)
        self.memory = ConversationBufferMemory(chat_memory=chat_memory, return_messages=True)

    def chat(self, message, engine, temperature):
        try:
            history = self.create_messages(message)
            self.load_memory(history)
            llm = ChatOpenAI(model_name=engines[engine]["name"], temperature=temperature, openai_api_key=openai.api_key)
            prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template(self.get_initial_prompt()),
                    MessagesPlaceholder(variable_name="history"),
                    HumanMessagePromptTemplate.from_template("{input}"),
                ]
            )
            conversation = ConversationChain(memory=self.memory, prompt=prompt, llm=llm)
            response_text = conversation.predict(input=message)
            self.add_to_history({"role": "assistant", "content": response_text})
            return response_text
        except Exception as e:
            error = f"I'm sorry, we got an error: \n {e}"
            self.add_to_history({"role": "system", "content": error})
            return error

    def get_history(self):
        return self.history

    def get_message(self, index):
        return self.history[index]

    def replace_message(self, index, message):
        self.history[index]["content"] = message

    def add_to_history(self, message):
        self.history.append(message)

    def remove_from_history(self, index):
        self.history.pop(index)
