"""
Main Streamlit application for RAG Chatbot.
"""

import streamlit as st

from config import PAGE_TITLE, PAGE_ICON
from llm.chain import create_chain, format_chat_history
from ui.ui import (
    render_sidebar,
    initialize_chat_history,
    display_chat_history,
    get_user_input,
    display_user_message,
    get_assistant_message_placeholder
)


# --- Page Config ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
st.title(f"{PAGE_ICON} Chat with your Data")

# --- Render Sidebar ---
render_sidebar()

# --- Setup Chain (Cached) ---
@st.cache_resource
def get_cached_chain(chat_history):
    """Get the cached RAG chain with chat history."""
    return create_chain(chat_history)


# Load the chain - refresh if documents were updated
if st.session_state.get("documents_updated", False):
    st.cache_resource.clear()
    st.session_state.documents_updated = False

# Format chat history for the chain
chat_history = format_chat_history(st.session_state.get("messages", []))
chain = get_cached_chain(chat_history)

if chain is None:
    st.warning("⚠️ No documents found. Please upload some PDFs or TXT files to get started.")
else:
    st.info("✅ Knowledge base is ready. Ask your questions!")

# --- Chat Interface ---
initialize_chat_history()
display_chat_history()

if question := get_user_input():
    display_user_message(question)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if chain:
            # Update chat history before generating response
            chat_history = format_chat_history(st.session_state.messages)
            # Create a fresh chain with updated history
            current_chain = create_chain(chat_history)
            
            if current_chain:
                full_response = ""
                for chunk in current_chain.stream(question):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            else:
                full_response = "Error: No chain available"
                message_placeholder.error("Chain not available. Please upload documents first.")
        else:
            full_response = "Error: No chain available"
            message_placeholder.error("Chain not available. Please upload documents first.")
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
