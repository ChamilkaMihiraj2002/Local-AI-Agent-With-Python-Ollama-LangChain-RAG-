# Quick Start Guide

## 🚀 Prerequisites

Before running the RAG chatbot, ensure you have:

1. **Ollama installed** - Download from [ollama.ai](https://ollama.ai)
2. **Python 3.11+** with virtual environment
3. **4GB+ RAM** for running models locally

## ⚙️ Initial Setup

### Step 1: Start Ollama Service
Open a terminal and run:
```bash
ollama serve
```

Wait for the output:
```
Listening on [::]:11434
```

### Step 2: Pull Required Models
In another terminal, run:
```bash
# Embedding model (required)
ollama pull mxbai-embed-large

# Language model (required)
ollama pull llama3.2
```

### Step 3: Verify Installation (Optional)
```bash
chmod +x verify-setup.sh
./verify-setup.sh
```

### Step 4: Install Python Dependencies
```bash
# Navigate to the project
cd /Users/chamilkamihiraj/Desktop/GitHub/Local-AI-Agent-With-Python-Ollama-LangChain-RAG-

# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Upload Documents
Place your PDF and TXT files in:
```
App/data/
```

### Step 6: Run the App
```bash
cd App
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Common Issues

### ❌ "Connection refused" or "Cannot connect to Ollama"
**Fix:** Make sure Ollama is running
```bash
ollama serve
```

### ❌ "Model not found: mxbai-embed-large"
**Fix:** Pull the embedding model
```bash
ollama pull mxbai-embed-large
```

### ❌ "Model not found: llama3.2"
**Fix:** Pull the LLM model
```bash
ollama pull llama3.2
```

### ❌ "No documents found"
**Fix:** Add PDF/TXT files to `App/data/` and refresh the knowledge base

For more troubleshooting, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

## 📋 Real-Time Features

### Upload Documents
1. Click the sidebar "Upload PDF or TXT" button
2. Select one or more files
3. Wait for "Upload complete" status
4. **Documents are immediately indexed** - no refresh needed!
5. Start asking questions right away

### Refresh Knowledge Base
Click "🔄 Refresh Knowledge Base" to rebuild the vector store with all documents

### Clear Everything
Click "🗑️ Clean Documents" to remove all documents and reset the database

## 🔧 Configuration

Edit `App/config.py` to customize:

```python
# Models
EMBEDDING_MODEL = "mxbai-embed-large"  # Change to other Ollama models
LLM_MODEL = "llama3.2"                 

# Document Processing
CHUNK_SIZE = 1000          # Size of text chunks for embedding
CHUNK_OVERLAP = 200        # Overlap between chunks
RETRIEVER_K = 5            # Number of chunks to retrieve per query

# Alternative Models (if you have memory constraints):
# EMBEDDING_MODEL = "nomic-embed-text"  # Smaller, faster
# EMBEDDING_MODEL = "all-minilm"        # Smallest
# LLM_MODEL = "mistral"                 # Smaller, faster
```

## 📊 Application Structure

```
App/
├── app.py              # Main Streamlit application
├── config.py           # Configuration settings
├── ui/
│   └── ui.py          # Sidebar and UI components
├── llm/
│   └── chain.py       # RAG chain setup
├── vector/
│   └── vector_store.py # Document embedding & storage
├── data/              # Your uploaded documents (add here)
└── db/                # Vector database (auto-created)
```

## 🎓 Usage Example

1. **Upload a PDF** about Python programming via sidebar
2. **Ask questions:**
   - "What is a decorator in Python?"
   - "Explain Python generators"
   - "Give me examples of list comprehensions"
3. **Real-time responses** from your uploaded documents

## 📈 Performance Tips

For better performance on limited hardware:

```python
# In App/config.py
CHUNK_SIZE = 500         # Smaller chunks = faster processing
RETRIEVER_K = 3          # Fewer results = faster queries
EMBEDDING_MODEL = "nomic-embed-text"  # Smaller model
```

## 🆘 Getting Help

1. Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. Run `./verify-setup.sh` to diagnose issues
3. Check Streamlit console for detailed error messages
4. Ensure Ollama service is running: `ollama serve`

## 🎉 You're Ready!

Now you have a local AI agent that can understand and answer questions about your documents!

### Quick Command Reference

```bash
# Start Ollama
ollama serve

# List installed models
ollama list

# Pull a model
ollama pull <model-name>

# Run the app
cd App && streamlit run app.py

# Run verification
chmod +x verify-setup.sh
./verify-setup.sh
```

Enjoy your local AI chatbot! 🚀
