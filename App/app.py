import os
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Import the function, not the variable
from vector import get_retriever

# --- Page Config ---
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 Chat with your Data")

# --- Sidebar: File Upload ---
with st.sidebar:
    st.header("📂 Manage Knowledge")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # 1. FIX: Get the absolute path where app.py is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. FIX: Point to the 'data' folder inside that specific directory
        data_dir = os.path.join(script_dir, "data")
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        for uploaded_file in uploaded_files:
            # 3. FIX: Save using the absolute path
            file_path = os.path.join(data_dir, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Debugging: Print to UI so you know exactly where it went
            st.success(f"Saved to: {file_path}")
            
    # Button to reload the vector database
    if st.button("🔄 Refresh Knowledge Base"):
        st.cache_resource.clear()
        st.success("Knowledge base refreshed!")

# --- 1. Setup Chain (Cached) ---
@st.cache_resource
def get_chain():
    # Load the retriever (this might take a moment if creating a new DB)
    retriever = get_retriever()
    
    if not retriever:
        return None

    llm = OllamaLLM(model="llama3.2")
    
    template = """
    You are a helpful assistant. Use the provided context to answer the question.
    If the answer is not in the context, simply say you don't know.
    
    Context:
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

# Load the chain
chain = get_chain()

# --- 2. Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if chain:
            message_placeholder.markdown("Thinking...")
            try:
                response = chain.invoke(question)
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                message_placeholder.error(f"Error: {e}")
        else:
            message_placeholder.error("Please upload a document to the sidebar first.")