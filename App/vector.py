import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# --- Configuration ---
# Get directory of this script (vector.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_LOCATION = os.path.join(BASE_DIR, "db", "chroma_db_generic")
EMBEDDING_MODEL = "mxbai-embed-large"

def get_vector_store():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Check if database already exists and has content
    if os.path.exists(DB_LOCATION) and os.listdir(DB_LOCATION):
        vector_store = Chroma(
            persist_directory=DB_LOCATION,
            embedding_function=embeddings,
            collection_name="generic_data"
        )
    else:
        # Create new store if it doesn't exist
        print("--- Creating new Vector Store ---")
        pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
        txt_loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
        
        docs = []
        try: docs.extend(pdf_loader.load())
        except: pass
        try: docs.extend(txt_loader.load())
        except: pass
            
        if not docs:
            return None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=DB_LOCATION,
            collection_name="generic_data"
        )
        
    return vector_store

def get_retriever():
    """
    Public function to get the retriever.
    """
    vector_store = get_vector_store()
    if vector_store:
        return vector_store.as_retriever(search_kwargs={"k": 5})
    return None