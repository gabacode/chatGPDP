import os
from langchain.chains.llm import LLMChain
import openai
from chatgpdp.modules.chat.embedder import Embedder

from chatgpdp.modules.utils.config import PATHS, engines
from langchain import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage
import traceback

from langchain.chains import (
    ConversationChain,
    ConversationalRetrievalChain,
)
from langchain.chat_models import ChatOpenAI
from langchain.llms import GPT4All
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage

from chatgpdp.modules.chat.embedder import Embedder
from chatgpdp.modules.utils.config import PATHS, engines
from chatgpdp.modules.utils.settings import Settings


def reload_env():
    key = Settings().get_by_key("OPENAI_API_KEY")
    openai.api_key = key


class Chatbot:
    embeds = Embedder()
    chatlogs_directory = PATHS["chatlogs"]
    screenshot_directory = PATHS["screenshots"]
    settings = Settings().get()

    def __init__(self, history):
        self.env_init()
        self.history = history
        self.chat_memory = ChatMessageHistory()
        self.memory = ConversationBufferMemory()

    def env_init(self):
        if not os.path.exists(self.chatlogs_directory):
            os.mkdir(self.chatlogs_directory)
        if not os.path.exists(self.screenshot_directory):
            os.mkdir(self.screenshot_directory)
        reload_env()

    def create_messages(self, prompt):
        self.add_to_history({"role": "user", "content": prompt})
        return self.history

    def get_initial_prompt(self):
        for message in self.history:
            if message["role"] == "system":
                return message["content"]

    def load_memory(self, history, return_messages=True):
        messages = []
        for message in history:
            if message["role"] == "user":
                messages.append(HumanMessage(content=message["content"], additional_kwargs={}))
            elif message["role"] == "assistant":
                messages.append(AIMessage(content=message["content"], additional_kwargs={}))
        self.chat_memory = ChatMessageHistory(messages=messages)
        self.memory = ConversationBufferMemory(chat_memory=self.chat_memory, return_messages=return_messages)

    def qa(self, message, engine, temperature, file_path):
        history = self.create_messages(message)
        self.load_memory(history)
        uploaded_file = open(file_path, "rb")
        uploaded_file.seek(0)
        file = uploaded_file.read()
        vectors = self.embeds.getDocEmbeds(file, uploaded_file.name)

        template = self.get_initial_prompt() + "\n"
        template += """
        Be as accurate as possible, if you are not sure, say 'I don't know'.
        QUESTION: {question}
        =========
        {summaries}
        =========
        ANSWER:
        """
        prompt = PromptTemplate(template=template, input_variables=["summaries", "question"])

        try:
            llm = ChatOpenAI(
                temperature=temperature,
                model_name=engines[engine]["name"],
                openai_api_key=openai.api_key,
                request_timeout=120,
                max_tokens=512,
            )

            question_generator = LLMChain(llm=llm, prompt=prompt)
            doc_chain = load_qa_with_sources_chain(llm, chain_type="stuff")

            qa = ConversationalRetrievalChain(
                retriever=vectors.as_retriever(),
                question_generator=question_generator,
                combine_docs_chain=doc_chain,
                return_source_documents=True,
            )
            result = qa({"question": message, "chat_history": []})
            response_text = result["answer"]
            self.add_to_history({"role": "user", "content": message})
            self.add_to_history({"role": "assistant", "content": response_text})
            return response_text
        except Exception as e:
            error = f"I'm sorry, we got an error: \n {e}"
            self.add_to_history({"role": "system", "content": error})
            return error

    def chat(self, message, engine, temperature):
        try:
            is_gpt = engines[engine]['name'].startswith("gpt-")

            if is_gpt:
                self.load_memory(self.history)
                prompt = ChatPromptTemplate.from_messages(
                    [
                        SystemMessagePromptTemplate.from_template(self.get_initial_prompt()),
                        MessagesPlaceholder(variable_name="history"),
                        HumanMessagePromptTemplate.from_template("{input}"),
                    ]
                )

                llm = ChatOpenAI(
                    model_name=engines[engine]["name"],
                    temperature=temperature,
                    openai_api_key=openai.api_key,
                    request_timeout=600,
                )

                conversation = ConversationChain(
                    memory=self.memory,
                    prompt=prompt,
                    llm=llm,
                    verbose=True
                )

                response = conversation.predict(input=message)

                self.add_to_history({"role": "user", "content": message})
                self.add_to_history({"role": "assistant", "content": response})

                return response

            else:
                self.load_memory(self.history, return_messages=is_gpt)
                model_name = engines[engine]["name"]
                model_path = os.path.join(PATHS["models"], model_name)

                if not os.path.exists(model_path):
                    model_path = model_name

                llm = GPT4All(
                    model=model_path,
                    backend="gptj",
                    temp=temperature,
                    n_threads=8,
                    n_predict=256,
                    max_tokens=engines[engine]["max_tokens"],
                    allow_download=True,
                )

                conversation = ConversationChain(
                    llm=llm,
                    memory=self.memory,
                    verbose=True,
                )
                response = (conversation.predict(input=message)).strip()

                self.add_to_history({"role": "user", "content": message})
                self.add_to_history({"role": "assistant", "content": response})

                return response

        except (TypeError, ValueError) as e:
            error = f"I'm sorry, we got an error: {e} \n {traceback.format_exc()}"
            self.add_to_history({"role": "system", "content": error})
            return error

    def get_history(self):
        return self.history

    def get_message(self, index):
        try:
            return self.history[index]
        except Exception as e:
            print(e)

    def replace_message(self, index, message):
        try:
            self.history[index]["content"] = message
        except Exception as e:
            print(e)

    def add_to_history(self, message):
        self.history.append(message)

    def remove_from_history(self, index):
        self.history.pop(index)
