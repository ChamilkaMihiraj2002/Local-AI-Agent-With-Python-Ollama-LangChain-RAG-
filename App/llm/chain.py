"""
LLM chain setup and management.
Handles the RAG (Retrieval-Augmented Generation) chain creation.
"""

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import LLM_MODEL
from vector.vector_store import get_retriever


def format_docs(docs):
    """Format retrieved documents into a string."""
    return "\n\n".join(doc.page_content for doc in docs)


def create_prompt_template():
    """Create the prompt template for the RAG chain with chat history."""
    template = """
    You are a helpful assistant. Use the provided context to answer the question.
    If the answer is not in the context, simply say you don't know.
    
    Context:
    {context}
    
    Chat History:
    {chat_history}
    
    Current Question: {question}
    
    Answer:
    """
    return ChatPromptTemplate.from_template(template)


def create_chain(chat_history=""):
    """
    Create the RAG chain with conversation memory.
    Returns the complete chain or None if retriever is not available.
    
    Args:
        chat_history: String containing the formatted chat history
    """
    retriever = get_retriever()
    
    if not retriever:
        return None

    llm = OllamaLLM(model=LLM_MODEL)
    prompt = create_prompt_template()

    chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough(),
            "chat_history": lambda x: chat_history
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


def format_chat_history(messages):
    """
    Format chat history from Streamlit session state.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
    
    Returns:
        Formatted string of chat history
    """
    if not messages:
        return "No previous conversation."
    
    formatted = []
    for msg in messages:
        role = "Human" if msg["role"] == "user" else "Assistant"
        formatted.append(f"{role}: {msg['content']}")
    
    return "\n".join(formatted)
