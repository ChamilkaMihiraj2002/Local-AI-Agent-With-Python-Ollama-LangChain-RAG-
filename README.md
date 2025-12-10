Local AI Agent With Python (Ollama, LangChain & RAG)

## About This App

This is a **Retrieval Augmented Generation (RAG) Chatbot** built entirely with open-source tools and running locally on your machine. It combines the power of LangChain, Ollama, and Streamlit to create an intelligent assistant that can answer questions based on your own documents.

### Key Features

- 🤖 **Local AI**: Uses Ollama and Llama 3.2 for completely private, offline inference
- 📚 **Document Intelligence**: Upload PDFs or TXT files and ask questions about their content
- 🔍 **Semantic Search**: Leverages vector embeddings for intelligent document retrieval
- 💬 **Conversational Interface**: Interactive chat interface built with Streamlit
- 🔐 **Privacy First**: All processing happens locally—no data sent to external services
- ⚡ **Fast & Efficient**: Uses Chroma vector database for optimized similarity search

### How It Works

1. **Upload Documents**: Add PDF or TXT files to build your knowledge base
2. **Vector Embedding**: Documents are split into chunks and converted to vector embeddings
3. **Retrieval**: When you ask a question, the system retrieves relevant document chunks
4. **Generation**: The LLM generates an answer based on the retrieved context and chat history
5. **Conversation**: Maintains chat history for context-aware multi-turn conversations

### Technology Stack

- **Streamlit**: Web UI framework
- **LangChain**: LLM orchestration and RAG pipeline
- **Ollama**: Local LLM runtime
- **Chroma**: Vector database
- **mxbai-embed-large**: Embedding model for semantic search

## How to Run

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **Ollama**: Download from [ollama.ai](https://ollama.ai)
- **Git**: For cloning the repository

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ChamilkaMihiraj2002/Local-AI-Agent-With-Python-Ollama-LangChain-RAG-.git
   cd Local-AI-Agent-With-Python-Ollama-LangChain-RAG-
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama**
   ```bash
   ollama serve
   ```
   In a new terminal, pull the required models:
   ```bash
   ollama pull llama3.2
   ollama pull mxbai-embed-large
   ```

4. **Run the Application**
   ```bash
   cd App
   streamlit run app.py
   ```

5. **Access the Application**
   - Open your browser and navigate to: `http://localhost:8501`
   - Start uploading documents and ask questions!

### Troubleshooting

- **Ollama Connection Issues**: Make sure Ollama is running (`ollama serve`)
- **Model Download Issues**: Run `ollama pull llama3.2` and `ollama pull mxbai-embed-large` manually
- **Port Already in Use**: Change Streamlit port with `streamlit run app.py --server.port 8502`

## Folder Structure

```
.
├── App/                          # Main application directory
│   ├── app.py                   # Main Streamlit application
│   ├── config.py                # Configuration settings
│   ├── data/                    # Uploaded documents storage
│   ├── db/                      # Vector database
│   │   └── chroma_db_generic/  # Chroma vector database
│   ├── llm/
│   │   └── chain.py             # RAG chain and LLM logic
│   └── ui/
│       └── ui.py                # Streamlit UI components
├── requirements.txt              # Python dependencies
├── README.md                      # This file
├── LICENSE                        # License information
├── QUICKSTART.md                  # Quick start guide
├── TROUBLESHOOTING.md             # Common issues and solutions
├── DATABASE_PERMISSION_FIX.md     # Database permission fixes
├── ERROR_FIXES.md                 # Error solutions
├── REALTIME_UPDATE_IMPLEMENTATION.md  # Real-time updates guide
└── verify-setup.sh               # Setup verification script
```

### Key Directories Explained
- **App/**: Contains the entire Streamlit application
- **App/data/**: Where uploaded PDF and TXT files are stored
- **App/db/**: Vector database storage for embeddings
- **App/llm/**: LLM chain logic and RAG implementation
- **App/ui/**: UI components and Streamlit interface logic

<img width="1408" height="748" alt="Screenshot 2025-12-10 at 6 03 29 PM" src="https://github.com/user-attachments/assets/57d92a1a-74b8-4acf-bba8-3536015ab5ca" />
<img width="1402" height="738" alt="Screenshot 2025-12-10 at 6 10 04 PM" src="https://github.com/user-attachments/assets/0ac20e98-565a-40f1-bfe9-d5bf426d2d54" />
