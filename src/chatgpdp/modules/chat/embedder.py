import os
import pickle
import tempfile
from langchain.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from chatgpdp.modules.utils.config import PATHS

from chatgpdp.modules.utils.settings import Settings


class Embedder:
    def __init__(self):
        self.PATH = PATHS["embeddings"]
        self.createEmbeddingsDir()
        self.key = Settings().get_by_key("OPENAI_API_KEY")

    def createEmbeddingsDir(self):
        """
        Creates a directory to store the embeddings vectors
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def storeDocEmbeds(self, file, filename):
        """
        Stores document embeddings using Langchain and FAISS
        """
        # Write the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name

        print("Loading the data...", str(tmp_file_path))

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500,
            chunk_overlap=100,
            length_function=len,
        )

        text_extensions = [".txt", ".php", ".sch"]

        # Load the data from the file using Langchain
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path=tmp_file_path)
            data = loader.load_and_split(text_splitter)
        elif filename.endswith(".csv"):
            loader = CSVLoader(file_path=tmp_file_path)
            data = loader.load_and_split(text_splitter)
        elif any(filename.endswith(ext) for ext in text_extensions):
            loader = TextLoader(file_path=tmp_file_path)
            data = loader.load_and_split(text_splitter)

        # Create an embeddings object using Langchain
        embeddings = OpenAIEmbeddings(openai_api_key=self.key)

        # Store the embeddings vectors using FAISS
        vectors = FAISS.from_documents(data, embeddings)
        os.remove(tmp_file_path)

        # Save the vectors to a pickle file
        with open(f"{self.PATH}/{filename}.pkl", "wb") as f:
            pickle.dump(vectors, f)

        print("Done!")

    def getDocEmbeds(self, file, filename):
        """
        Retrieves document embeddings
        """
        formatted_filename = filename.split("/")[-1]
        # Check if embeddings vectors have already been stored in a pickle file
        if not os.path.isfile(f"{self.PATH}/{formatted_filename}.pkl"):
            # If not, store the vectors using the storeDocEmbeds function
            self.storeDocEmbeds(file, formatted_filename)

        # Load the vectors from the pickle file
        with open(f"{self.PATH}/{formatted_filename}.pkl", "rb") as f:
            vectors = pickle.load(f)

        return vectors
