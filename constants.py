import os

from chromadb.config import Settings

import defaults

# Define the folder for storing database
PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY', defaults.PERSIST_DIRECTORY)

# Define the Chroma settings
CHROMA_SETTINGS = Settings(persist_directory=PERSIST_DIRECTORY, anonymized_telemetry=False)