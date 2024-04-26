# All the magic strings in one place

PERSIST_DIRECTORY = 'db'
SOURCE_DIRECTORY = 'source_documents'
TARGET_SOURCE_CHUNKS = 4

# For embeddings model, the example uses a sentence-transformers model
# https://www.sbert.net/docs/pretrained_models.html 
# "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster and still offers good quality."

EMBEDDINGS_MODEL_NAME = 'all-MiniLM-L6-v2'

# Ollama based stuff

MODEL = 'mistral'
OLLAMA_BASE_URL = 'http://localhost:11434'
