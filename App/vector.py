import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# --- Configuration ---
DATA_DIR = "./data"
DB_LOCATION = "./db/chroma_db_generic"
EMBEDDING_MODEL = "mxbai-embed-large"

def get_vector_store():
    """
    Returns the vector store. 
    If the DB doesn't exist, it creates it by loading files from the DATA_DIR.
    """
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Check if database already exists and has content
    if os.path.exists(DB_LOCATION) and os.listdir(DB_LOCATION):
        print("--- Loading existing Vector Store ---")
        vector_store = Chroma(
            persist_directory=DB_LOCATION,
            embedding_function=embeddings,
            collection_name="generic_data"
        )
    else:
        print("--- Creating new Vector Store from data/ ---")
        
        # 1. Load Documents (PDFs and Text files)
        # We define separate loaders for different file types
        pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
        txt_loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
        
        docs = []
        try:
            docs.extend(pdf_loader.load())
        except Exception:
            pass # No PDFs found
            
        try:
            docs.extend(txt_loader.load())
        except Exception:
            pass # No Text files found
            
        if not docs:
            print(f"Warning: No documents found in {DATA_DIR}. Please add .txt or .pdf files.")
            # Return an empty store or handle gracefully
            return Chroma(embedding_function=embeddings, persist_directory=DB_LOCATION)

        # 2. Split Documents into chunks
        # Chunking is crucial for generic data (books, reports) unlike short tweets
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )
        splits = text_splitter.split_documents(docs)
        print(f"--- Processed {len(splits)} document chunks ---")

        # 3. Create and Persist Vector Store
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=DB_LOCATION,
            collection_name="generic_data"
        )
        
    return vector_store

# Initialize and export the retriever
# This code runs automatically when you import 'retriever' in main.py
try:
    _vector_store = get_vector_store()
    retriever = _vector_store.as_retriever(search_kwargs={"k": 5})
except Exception as e:
    print(f"Error initializing vector store: {e}")
    retriever = None