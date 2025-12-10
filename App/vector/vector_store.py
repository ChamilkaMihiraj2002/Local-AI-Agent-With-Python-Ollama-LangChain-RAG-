"""
Vector store and document handling module.
Manages document loading, embedding, and retrieval.
"""

import os
import shutil
import stat
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from config import DATA_DIR, DB_LOCATION, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVER_K


def ensure_writable_directory(directory_path):
    """
    Ensure directory exists and is writable.
    Fixes permission issues with the database directory.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)
        
        # Make directory writable (755 permissions)
        os.chmod(directory_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        
        # Make all files in directory writable
        for root, dirs, files in os.walk(directory_path):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.chmod(dir_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            
            for file_name in files:
                file_path = os.path.join(root, file_name)
                os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not fix directory permissions: {e}")
        return False


def load_documents():
    """Load PDF and TXT documents from the data directory."""
    docs = []
    
    try:
        pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
        docs.extend(pdf_loader.load())
    except Exception as e:
        print(f"Warning: Could not load PDFs: {e}")
    
    try:
        txt_loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
        docs.extend(txt_loader.load())
    except Exception as e:
        print(f"Warning: Could not load TXTs: {e}")
    
    return docs


def split_documents(docs):
    """Split documents into chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_documents(docs)


def get_embeddings():
    """Get the embedding model instance."""
    return OllamaEmbeddings(model=EMBEDDING_MODEL)


def get_vector_store():
    """
    Get or create the vector store.
    Returns the Chroma vector store instance.
    """
    try:
        embeddings = get_embeddings()
    except Exception as e:
        print(f"❌ Error initializing embeddings: {e}")
        print("⚠️ Make sure Ollama is running: ollama serve")
        return None
    
    # Check if database already exists and has content
    if os.path.exists(DB_LOCATION) and os.listdir(DB_LOCATION):
        try:
            # Fix permissions on existing database
            ensure_writable_directory(DB_LOCATION)
            
            vector_store = Chroma(
                persist_directory=DB_LOCATION,
                embedding_function=embeddings,
                collection_name="generic_data"
            )
            return vector_store
        except Exception as e:
            print(f"⚠️ Could not load existing vector store: {e}")
            print("🔄 Will rebuild vector store from documents...")
            # Fall through to rebuild
    
    # Create new store if it doesn't exist
    try:
        print("--- Creating new Vector Store ---")
        
        # Ensure database directory is writable
        ensure_writable_directory(DB_LOCATION)
        
        docs = load_documents()
        
        if not docs:
            print("❌ No documents found in data directory.")
            return None

        print(f"📄 Loaded {len(docs)} documents")
        splits = split_documents(docs)
        print(f"✂️  Split into {len(splits)} chunks")
        
        print(f"🔨 Creating Chroma vector store...")
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=DB_LOCATION,
            collection_name="generic_data"
        )
        
        # Fix permissions on newly created database
        ensure_writable_directory(DB_LOCATION)
        
        print(f"✅ Vector store created successfully!")
        return vector_store
        
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        print("⚠️ Possible causes:")
        print("  1. Ollama service is not running")
        print("  2. Embedding model is not installed")
        print("  3. Database directory has permission issues")
        print("  4. Documents are empty or corrupted")
        print("\n💡 Try running:")
        print("  • Fix permissions: chmod -R u+w App/db/")
        print("  • Start Ollama: ollama serve")
        print("  • Pull model: ollama pull mxbai-embed-large")
        return None


def get_retriever():
    """
    Get the retriever for document similarity search.
    Returns a retriever instance or None if no vector store exists.
    """
    vector_store = get_vector_store()
    if vector_store:
        return vector_store.as_retriever(search_kwargs={"k": RETRIEVER_K})
    return None


def rebuild_vector_store():
    """
    Rebuild the vector store from scratch.
    This is called when new documents are uploaded to ensure real-time updates.
    """
    try:
        print("--- Rebuilding Vector Store ---")
        
        # Clear existing database with proper permission handling
        if os.path.exists(DB_LOCATION):
            print(f"🔐 Fixing database permissions...")
            ensure_writable_directory(DB_LOCATION)
            
            print(f"🗑️  Removing old database...")
            try:
                shutil.rmtree(DB_LOCATION)
                print(f"✅ Cleared existing database")
            except PermissionError as pe:
                print(f"⚠️  Permission denied while removing database: {pe}")
                print("💡 Attempting alternative cleanup...")
                # Try removing with chmod
                for root, dirs, files in os.walk(DB_LOCATION, topdown=False):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR)
                            os.remove(file_path)
                        except Exception as e:
                            print(f"  ⚠️  Could not remove {file}: {e}")
                    
                    for dir_name in dirs:
                        try:
                            dir_path = os.path.join(root, dir_name)
                            os.chmod(dir_path, stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)
                            os.rmdir(dir_path)
                        except Exception as e:
                            print(f"  ⚠️  Could not remove {dir_name}: {e}")
                
                try:
                    os.chmod(DB_LOCATION, stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)
                    os.rmdir(DB_LOCATION)
                except Exception as e:
                    print(f"  ⚠️  Could not remove root db directory: {e}")
        
        # Ensure database directory is writable
        print(f"🔧 Setting up database directory permissions...")
        ensure_writable_directory(DB_LOCATION)
        
        # Create new store with latest documents
        try:
            embeddings = get_embeddings()
        except Exception as e:
            print(f"❌ Error initializing embeddings: {e}")
            print("⚠️ Make sure Ollama is running: ollama serve")
            raise
        
        docs = load_documents()
        
        if not docs:
            print("❌ No documents found in data directory.")
            return None
        
        print(f"📄 Loaded {len(docs)} documents")
        splits = split_documents(docs)
        print(f"✂️  Split into {len(splits)} document chunks...")
        
        print(f"🔨 Creating vector store with embeddings...")
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=DB_LOCATION,
            collection_name="generic_data"
        )
        
        # Fix permissions on newly created database
        print(f"🔐 Fixing new database permissions...")
        ensure_writable_directory(DB_LOCATION)
        
        print(f"✅ Vector store rebuilt successfully with {len(splits)} chunks")
        return vector_store
        
    except Exception as e:
        print(f"❌ Error rebuilding vector store: {e}")
        print("⚠️ Possible causes:")
        print("  1. Ollama service is not running")
        print("  2. Embedding model is not installed")
        print("  3. Database directory has permission issues")
        print("  4. Disk space is full")
        print("\n💡 Troubleshooting:")
        print("  • Check Ollama: ps aux | grep ollama")
        print("  • Fix permissions: chmod -R u+w App/db/")
        print("  • Start Ollama: ollama serve")
        print("  • Pull model: ollama pull mxbai-embed-large")
        raise
