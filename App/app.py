import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Import your existing retriever logic
# Note: This will run the vector.py initialization code
from vector import retriever

# --- Page Config ---
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 Chat with your Data")

# --- 1. Setup Chain (Cached) ---
# We use @st.cache_resource so we don't reload the LLM/Chain on every user interaction
@st.cache_resource
def get_chain():
    # 1. LLM
    llm = OllamaLLM(model="llama3.2")
    
    # 2. Prompt
    template = """
    You are a helpful assistant. Use the provided context to answer the question.
    If the answer is not in the context, simply say you don't know.
    
    Context:
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # 3. Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

chain = get_chain()

# --- 2. Session State (Memory) ---
# Streamlit reruns the script on every interaction, so we need to save chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Handle User Input ---
if question := st.chat_input("Ask a question about your documents..."):
    # A. Display user message
    with st.chat_message("user"):
        st.markdown(question)
    
    # B. Add user message to history
    st.session_state.messages.append({"role": "user", "content": question})

    # C. Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Invoke the chain
            response = chain.invoke(question)
            message_placeholder.markdown(response)
            
            # D. Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            message_placeholder.error(f"Error: {e}")