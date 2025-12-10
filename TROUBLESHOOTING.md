# Troubleshooting Guide

## Issue: Chroma Vector Store Error

### Error Message
```
Error creating/rebuilding vector store
Connection refused / Cannot connect to Ollama
```

### Root Cause
The Ollama service (which provides the embedding model) is not running.

### Solution

#### 1. **Check if Ollama is Running**
```bash
ps aux | grep ollama
```

If no output, Ollama is not running.

#### 2. **Start Ollama Service**
```bash
ollama serve
```

This will start the Ollama service on `http://localhost:11434`

#### 3. **Verify Embedding Model is Installed**
```bash
ollama list
```

Look for `mxbai-embed-large` in the list.

#### 4. **Pull the Embedding Model (if missing)**
```bash
ollama pull mxbai-embed-large
```

#### 5. **Verify LLM Model is Installed**
```bash
ollama list
```

Look for `llama3.2` in the list.

#### 6. **Pull the LLM Model (if missing)**
```bash
ollama pull llama3.2
```

### Complete Startup Sequence

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```

Wait for it to show:
```
Listening on [::]:11434
```

**Terminal 2 - Start Streamlit App:**
```bash
cd /Users/chamilkamihiraj/Desktop/GitHub/Local-AI-Agent-With-Python-Ollama-LangChain-RAG-/App
streamlit run app.py
```

### Verification Checklist

✅ Ollama service is running
```bash
curl http://localhost:11434/api/version
```

✅ Embedding model is available
```bash
curl -X POST http://localhost:11434/api/embed -d '{"model":"mxbai-embed-large","input":"test"}'
```

✅ LLM model is available
```bash
ollama list | grep llama
```

### If Issues Persist

1. **Restart Ollama:**
   ```bash
   # Kill existing Ollama process
   pkill -f ollama
   
   # Start fresh
   ollama serve
   ```

2. **Clear Vector Store and Restart:**
   ```bash
   # Remove the database
   rm -rf /Users/chamilkamihiraj/Desktop/GitHub/Local-AI-Agent-With-Python-Ollama-LangChain-RAG-/App/db/chroma_db_generic
   
   # Restart app - it will rebuild from documents
   ```

3. **Check System Resources:**
   - Ensure you have enough disk space
   - Check available RAM (Ollama requires ~4GB)
   - Monitor CPU usage: `top` or `Activity Monitor`

### Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Ollama not running | Connection refused | `ollama serve` |
| Model not installed | Unknown model | `ollama pull mxbai-embed-large` |
| Wrong model name | Model not found | Check config.py EMBEDDING_MODEL |
| Port already in use | Address already in use | Change Ollama port or kill process |
| Out of memory | Process killed | Increase system RAM or reduce CHUNK_SIZE |

### Configuration

Adjust these in `config.py` if needed:

```python
# Embedding Configuration
EMBEDDING_MODEL = "mxbai-embed-large"  # Change to another model if preferred
LLM_MODEL = "llama3.2"                  # Change to another LLM if preferred

# Document Processing
CHUNK_SIZE = 1000      # Reduce if memory issues
CHUNK_OVERLAP = 200
RETRIEVER_K = 5        # Number of chunks to retrieve

# Alternative Models

# Embedding Models (smaller/faster):
# - nomic-embed-text (recommended for low RAM)
# - all-minilm (smallest)
# - mxbai-embed-large (current - better quality)

# LLM Models:
# - mistral (faster, less capable)
# - neural-chat (balanced)
# - llama3.2 (current - recommended)
# - dolphin-mixtral (very capable, needs more RAM)
```

### Alternative Embedding Models

If you have memory constraints:

```bash
# Smallest and fastest
ollama pull all-minilm

# Good balance
ollama pull nomic-embed-text

# Current (recommended)
ollama pull mxbai-embed-large
```

Then update `config.py`:
```python
EMBEDDING_MODEL = "nomic-embed-text"  # or other model
```

### Performance Tips

1. **Reduce Chunk Size** (if slow):
   ```python
   CHUNK_SIZE = 500  # Instead of 1000
   ```

2. **Reduce Retrieved Chunks**:
   ```python
   RETRIEVER_K = 3  # Instead of 5
   ```

3. **Use Faster Model**:
   ```python
   EMBEDDING_MODEL = "nomic-embed-text"
   ```

### Debug Mode

Run with verbose logging:
```bash
# In the App directory, run with debug output
python -c "from vector.vector_store import get_vector_store; print(get_vector_store())"
```

### Need Help?

Check the logs in the Streamlit terminal for detailed error messages. The app now provides better error diagnostics to help identify the issue.
