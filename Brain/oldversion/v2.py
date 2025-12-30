import json
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import os
import argparse
import time

load_dotenv()

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))

from Brain.constants import CHROMA_SETTINGS

conversation_history_file = "Brain\\conversation_history"


def main(question, prompt, word_limit=30):
    # Parse the command line arguments
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    # Prepare the LLM
    match model_type:
        case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False)
        case "GPT4All":
            llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', n_batch=model_n_batch, callbacks=callbacks, verbose=False)
        case _default:
            print(f"Model {model_type} not supported!")
            exit()

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not args.hide_source)

    # Load conversation history
    conversation_history = load_conversation_history()

    # Interactive questions and answers
    while True:
        query = question
        if query == "exit":
            break
        if query.strip() == "":
            continue

        # Construct the input prompt
        input_prompt = f"{prompt} {query}"

        # Search in conversation history first
        previous_exchange = find_previous_exchange(conversation_history, query)
        if previous_exchange:
            return previous_exchange['system']

        # Get the answer from the chain
        start = time.time()
        res = qa(input_prompt)
        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        end = time.time()

        # Update conversation history
        conversation_history.append({'user': query, 'system': answer})
        save_conversation_history(conversation_history)
        
        # Add a full stop at the end of the answer if it is missing
        if not answer.endswith('.'):
           answer += '.'
           
        # Limit the answer to the specified word limit
        if word_limit is not None:
            answer_words = answer.split()
            answer = ' '.join(answer_words[:word_limit])

        return answer


def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()


def load_conversation_history():
    if os.path.exists(conversation_history_file):
        try:
            with open(conversation_history_file, "r") as file:
                return json.load(file)
        except json.decoder.JSONDecodeError:
            # If the file is empty or not valid JSON, return an empty list
            return []
    else:
        return []


def save_conversation_history(conversation_history):
    with open(conversation_history_file, "w") as file:
        json.dump(conversation_history, file)


def find_previous_exchange(conversation_history, question):
    for exchange in reversed(conversation_history):
        if exchange['user'] == question:
            return exchange
    return None

'''
# Example usage
question = input("enter : ")
prompt = "Please provide accurate and concise information about the topic in 30 words:"
answer = main(question, prompt, word_limit=30)
'''
