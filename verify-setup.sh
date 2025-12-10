#!/bin/bash
# Setup verification script for RAG Chatbot

echo "🔍 RAG Chatbot - Setup Verification"
echo "===================================="
echo ""

# Check if Ollama is running
echo "1️⃣  Checking if Ollama is running..."
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    VERSION=$(curl -s http://localhost:11434/api/version | grep -o '"version":"[^"]*' | cut -d'"' -f4)
    echo "   Version: $VERSION"
else
    echo "❌ Ollama is NOT running"
    echo "   💡 Fix: Run 'ollama serve' in another terminal"
fi

echo ""

# Check if mxbai-embed-large is installed
echo "2️⃣  Checking for embedding model (mxbai-embed-large)..."
if command -v ollama &> /dev/null; then
    if ollama list | grep -q "mxbai-embed-large"; then
        echo "✅ Embedding model found"
    else
        echo "❌ Embedding model NOT found"
        echo "   💡 Fix: Run 'ollama pull mxbai-embed-large'"
    fi
else
    echo "⚠️  Ollama CLI not in PATH"
    echo "   💡 Make sure Ollama is properly installed"
fi

echo ""

# Check if llama3.2 is installed
echo "3️⃣  Checking for LLM model (llama3.2)..."
if command -v ollama &> /dev/null; then
    if ollama list | grep -q "llama3.2"; then
        echo "✅ LLM model found"
    else
        echo "⚠️  LLM model NOT found"
        echo "   💡 Note: This is optional, app can run without it initially"
        echo "   💡 Install: 'ollama pull llama3.2'"
    fi
fi

echo ""

# Check Python environment
echo "4️⃣  Checking Python environment..."
if [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
    echo "✅ Virtual environment found"
else
    PYTHON="python3"
    echo "⚠️  Virtual environment not found in venv/"
fi

echo ""

# Check required Python packages
echo "5️⃣  Checking Python dependencies..."
PACKAGES=("streamlit" "langchain" "langchain-community" "langchain-chroma" "langchain-ollama")

for package in "${PACKAGES[@]}"; do
    if $PYTHON -c "import ${package//-/_}" 2>/dev/null; then
        echo "✅ $package"
    else
        echo "❌ $package NOT installed"
    fi
done

echo ""

# Check data directory
echo "6️⃣  Checking data directory..."
if [ -d "App/data" ]; then
    COUNT=$(find "App/data" -type f \( -name "*.pdf" -o -name "*.txt" \) | wc -l)
    echo "✅ Data directory exists"
    echo "   Documents: $COUNT files"
else
    echo "⚠️  Data directory not found"
    echo "   💡 Create it with: mkdir -p App/data"
fi

echo ""

# Check database directory
echo "7️⃣  Checking database..."
if [ -d "App/db/chroma_db_generic" ]; then
    echo "✅ Vector database found"
else
    echo "ℹ️  Vector database not yet created (will be created on first run)"
fi

echo ""
echo "===================================="
echo "✅ Verification Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Ensure Ollama is running: ollama serve"
echo "2. Pull required models if needed"
echo "3. Upload documents to App/data/"
echo "4. Run: streamlit run App/app.py"
