import json
import os
import argparse
import time
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp

load_dotenv()

# Constants
EMBEDDINGS_MODEL_NAME = os.environ.get("EMBEDDINGS_MODEL_NAME")
PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY')
MODEL_TYPE = os.environ.get('MODEL_TYPE')
MODEL_PATH = os.environ.get('MODEL_PATH')
MODEL_N_CTX = os.environ.get('MODEL_N_CTX')
MODEL_N_BATCH = int(os.environ.get('MODEL_N_BATCH', 8))
TARGET_SOURCE_CHUNKS = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))
CONVERSATION_HISTORY_FILE = "Brain\\data.json"
CHROMA_SETTINGS = ...

from constants import CHROMA_SETTINGS
from functools import lru_cache
class AIChatBot:
    def __init__(self):
        self.qa = None
        self.conversation_history = []

    def initialize(self, args):
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
        
        # Initialize the retriever
        db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
        retriever = db.as_retriever(search_kwargs={"k": TARGET_SOURCE_CHUNKS})
        
        # Activate/deactivate the streaming StdOut callback for LLMs
        callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
        
        # Prepare the LLM
        if MODEL_TYPE == "LlamaCpp":
            llm = LlamaCpp(model_path=MODEL_PATH, n_ctx=MODEL_N_CTX, n_batch=MODEL_N_BATCH, callbacks=callbacks, verbose=False)
        elif MODEL_TYPE == "GPT4All":
            llm = GPT4All(model=MODEL_PATH, n_ctx=MODEL_N_CTX, backend='gptj', n_batch=MODEL_N_BATCH, callbacks=callbacks, verbose=False)
        else:
            raise ValueError(f"Model {MODEL_TYPE} not supported!")
        
        # Initialize the QA systeme
        self.qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not args.hide_source)
        
        # Load conversation history
        self.conversation_history = self.load_conversation_history()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                     'using the power of LLMs.')
        parser.add_argument("--hide-source", "-S", action='store_true',
                            help='Use this flag to disable printing of source documents used for answers.')
        parser.add_argument("--mute-stream", "-M",
                            action='store_true',
                            help='Use this flag to disable the streaming StdOut callback for LLMs.')
        return parser.parse_args()

    def load_conversation_history(self):
        if os.path.exists(CONVERSATION_HISTORY_FILE):
            try:
                with open(CONVERSATION_HISTORY_FILE, "r") as file:
                    return json.load(file)
            except json.decoder.JSONDecodeError:
                # If the file is empty or not valid JSON, return an empty list
                return []
        else:
            return []

    def save_conversation_history(self):
        with open(CONVERSATION_HISTORY_FILE, "w") as file:
            json.dump(self.conversation_history, file)

    def find_previous_exchange(self, question):
        for exchange in reversed(self.conversation_history):
            if exchange['user'] == question:
                return exchange
        return None
    
    @lru_cache(maxsize=128)  # Adjust maxsize as needed
    def compute_answer(self, question, prompt, word_limit=30, hide_source=False):
        # Construct the input prompt
        input_prompt = f"{prompt} {question}"

        # Get the answer from the chain
        res = self.qa(input_prompt)
        answer, docs = res['result'], [] if hide_source else res['source_documents']

        # Add a full stop at the end of the answer if it is missing
        if not answer.endswith('.'):
            answer += '.'

        # Limit the answer to the specified word limit
        if word_limit is not None:
            answer_words = answer.split()
            answer = ' '.join(answer_words[:word_limit])

        return answer

    def ask_question(self, question, prompt, word_limit=30, args=None):
        # Search in conversation history first
        previous_exchange = self.find_previous_exchange(question)
        if previous_exchange:
            return previous_exchange['system']

        # Compute the answer (this is the part that is cached)
        answer = self.compute_answer(question, prompt, word_limit, args.hide_source)

        # Update conversation history
        self.conversation_history.append({'user': question, 'system': answer})
        self.save_conversation_history()

        return answer

def main(question):
    chatbot = AIChatBot()
    args = chatbot.parse_arguments()
    chatbot.initialize(args)
    
    # Example usage
    prompt = "Please provide accurate and concise information about the topic in 30 words:"
    answer = chatbot.ask_question(question, prompt, word_limit=30, args=args)
    return answer
    


while True:
    answer=input("enter :")
    print[main(answer)]
