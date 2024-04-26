#!/usr/bin/env python3

from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import Ollama

import chromadb
import os
import argparse
import time

import defaults
from constants import CHROMA_SETTINGS

model = os.environ.get('MODEL', defaults.MODEL)
ollama_base_url = os.environ.get('OLLAMA_BASE_URL', defaults.OLLAMA_BASE_URL)
embeddings_model_name = os.environ.get('EMBEDDINGS_MODEL_NAME', defaults.EMBEDDINGS_MODEL_NAME)
persist_directory = os.environ.get('PERSIST_DIRECTORY', defaults.PERSIST_DIRECTORY)
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',defaults.TARGET_SOURCE_CHUNKS))

def main():
    # Parse the command line arguments
    args = parse_arguments()

    print(f"MODEL .................: {model}")
    print(f"OLLAMA_BASE_URL .......: {ollama_base_url}")
    print(f"EMBEDDINGS_MODEL_NAME .: {embeddings_model_name}")
    print(f"PERSIST_DIRECTORY .....: {persist_directory}")
    print(f"TARGET_SOURCE_CHUNKS ..: {target_source_chunks}")
    print(f"Hide the sources ......: {args.hide_source}")
    print(f"Mute stream ...........: {args.mute_stream}")
    print(f"Setup embeddings ......: {args.setup_embeddings}")
    print()

    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    if args.setup_embeddings:
        return

    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    retriever = db.as_retriever(search_kwargs={'k': target_source_chunks})
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]

    llm = Ollama(model=model, callbacks=callbacks, base_url=ollama_base_url)

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever, return_source_documents= not args.hide_source)
    # Interactive questions and answers
    while True:
        query = input("\nEnter a query: ")
        if query == 'exit':
            break
        if query.strip() == '':
            continue

        # Get the answer from the chain
        start = time.time()
        res = qa(query)
        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        end = time.time()

        # Print the result
        print("\n\n> Question:")
        print(query.strip())
        print("\n\n> Answer:")
        print(answer.strip())

        # Print the relevant sources used for the answer
        for document in docs:
            print("\n> " + document.metadata['source'] + ':')
            print(document.page_content)

def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')

    parser.add_argument('--hide-source', '-S',
                        action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument('--mute-stream', '-M',
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    parser.add_argument('--setup-embeddings', '-E',
                        action='store_true',
                        help='Halt after loading the embeddings. This allows them to be saved in a docker image.')

    return parser.parse_args()


if __name__ == '__main__':
    main()