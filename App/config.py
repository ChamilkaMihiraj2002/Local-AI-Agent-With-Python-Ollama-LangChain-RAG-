"""
Configuration settings for the RAG chatbot application.
"""

import os

# Get directory of the App folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path configurations
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_LOCATION = os.path.join(BASE_DIR, "db", "chroma_db_generic")

# Model configurations
EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3.2"

# RAG parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 5

# Streamlit configuration
PAGE_TITLE = "RAG Chatbot"
PAGE_ICON = "🤖"
