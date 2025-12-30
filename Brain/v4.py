import json
import os
import argparse
import time
import logging
import yaml
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import Chroma
from langchain_community.llms import GPT4All
from langchain_community.llms import LlamaCpp



load_dotenv()
 
 
# Constants
EMBEDDINGS_MODEL_NAME = os.environ.get("EMBEDDINGS_MODEL_NAME")
PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY')
MODEL_TYPE = os.environ.get('MODEL_TYPE')
MODEL_PATH = os.environ.get('MODEL_PATH')
MODEL_N_CTX = os.environ.get('MODEL_N_CTX')
MODEL_N_BATCH = int(os.environ.get('MODEL_N_BATCH', 8))
TARGET_SOURCE_CHUNKS = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))
CONVERSATION_HISTORY_FILE = "Brain/data.json"
CHROMA_SETTINGS = ...

class AIChatBot:
    def __init__(self, config):
        self.config = config
        self.qa = None
        self.conversation_history = []
        self.logger = self.setup_logging()

    def setup_logging(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Add a stream handler for console logging
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def initialize(self, args):
        try:
            # Initialize embeddings
            embeddings = HuggingFaceEmbeddings(model_name=self.config.get("EMBEDDINGS_MODEL_NAME", EMBEDDINGS_MODEL_NAME))
        
            # Initialize the retriever
            db = Chroma(persist_directory=self.config.get("PERSIST_DIRECTORY", PERSIST_DIRECTORY),
                        embedding_function=embeddings,
                        client_settings=self.config.get("CHROMA_SETTINGS", CHROMA_SETTINGS))
            retriever = db.as_retriever(search_kwargs={"k": self.config.get("TARGET_SOURCE_CHUNKS", TARGET_SOURCE_CHUNKS)})
            
            # Activate/deactivate the streaming StdOut callback for LLMs
            callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
            
            # Prepare the LLM
            if self.config.get("MODEL_TYPE", MODEL_TYPE) == "LlamaCpp":
                llm = LlamaCpp(model_path=self.config.get("MODEL_PATH", MODEL_PATH),
                               n_ctx=self.config.get("MODEL_N_CTX", MODEL_N_CTX),
                               n_batch=self.config.get("MODEL_N_BATCH", MODEL_N_BATCH),
                               callbacks=callbacks, verbose=False)
            elif self.config.get("MODEL_TYPE", MODEL_TYPE) == "GPT4All":
                llm = GPT4All(model=self.config.get("MODEL_PATH", MODEL_PATH),
                              n_ctx=self.config.get("MODEL_N_CTX", MODEL_N_CTX),
                              backend='gptj',
                              n_batch=self.config.get("MODEL_N_BATCH", MODEL_N_BATCH),
                              callbacks=callbacks, verbose=False)
            else:
                raise ValueError(f"Model {self.config.get('MODEL_TYPE', MODEL_TYPE)} not supported!")
            
            # Initialize the QA system
            self.qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff",
                                                  retriever=retriever, return_source_documents=not args.hide_source)
            
            # Load conversation history
            self.conversation_history = self.load_conversation_history()

        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            raise

    

def main(question):
    config = AIChatBot.load_config("config.yml")  # Load configuration from a YAML file
    chatbot = AIChatBot(config)
    args = chatbot.parse_arguments()
    chatbot.initialize(args)
    

if __name__ == "__main__":
    main("what is ai")

