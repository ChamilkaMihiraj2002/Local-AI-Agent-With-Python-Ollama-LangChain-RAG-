"""
UI components and sidebar management.
Handles file uploads and knowledge base management.
"""

import os
import shutil
import streamlit as st

from config import DATA_DIR, DB_LOCATION


def ensure_data_directory():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def count_documents():
    """Count the number of PDF and TXT documents in the data directory."""
    ensure_data_directory()
    doc_count = 0
    for file in os.listdir(DATA_DIR):
        if file.endswith(('.pdf', '.txt')):
            doc_count += 1
    return doc_count


def clear_documents():
    """Clear all documents from data directory and vector database."""
    import stat
    
    # Clear data directory
    if os.path.exists(DATA_DIR):
        try:
            for file in os.listdir(DATA_DIR):
                file_path = os.path.join(DATA_DIR, file)
                try:
                    # Fix permissions before deletion
                    os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        st.write(f"✅ Removed: {file}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        st.write(f"✅ Removed folder: {file}")
                except Exception as e:
                    st.warning(f"Could not remove {file}: {e}")
        except Exception as e:
            st.error(f"Error clearing data directory: {e}")
    
    # Clear vector database with proper permission handling
    if os.path.exists(DB_LOCATION):
        try:
            for root, dirs, files in os.walk(DB_LOCATION, topdown=False):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR)
                        os.remove(file_path)
                    except Exception as e:
                        st.warning(f"Could not remove {file}: {e}")
                
                for dir_name in dirs:
                    try:
                        dir_path = os.path.join(root, dir_name)
                        os.chmod(dir_path, stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)
                        os.rmdir(dir_path)
                    except Exception as e:
                        st.warning(f"Could not remove {dir_name}: {e}")
            
            # Remove root directory
            os.chmod(DB_LOCATION, stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)
            os.rmdir(DB_LOCATION)
            st.write("✅ Vector database cleared!")
        except Exception as e:
            st.warning(f"Could not fully clear database: {e}")
            st.info("💡 Try running: `chmod -R u+w App/db/` then refresh")
    
    # Recreate db directory
    os.makedirs(DB_LOCATION, exist_ok=True)



def handle_file_upload():
    """Handle file upload from sidebar with real-time vector store updates."""
    from vector.vector_store import rebuild_vector_store
    
    ensure_data_directory()
    
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        upload_status = st.status("Processing uploads...", expanded=False)
        
        for uploaded_file in uploaded_files:
            file_path = os.path.join(DATA_DIR, uploaded_file.name)
            
            with upload_status:
                st.write(f"📥 Uploading {uploaded_file.name}...")
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.write(f"✅ Saved: {uploaded_file.name}")
        
        # Real-time vector store update
        with upload_status:
            st.write("🔄 Updating knowledge base...")
            try:
                rebuild_vector_store()
                st.session_state.documents_updated = True
                st.write("✅ Knowledge base updated successfully!")
                upload_status.update(label="Upload complete", state="complete")
            except Exception as e:
                error_msg = str(e)
                st.write(f"❌ Error updating knowledge base")
                st.write(f"📋 Details: {error_msg[:200]}")
                
                # Diagnose specific errors
                if "readonly" in error_msg.lower() or "permission" in error_msg.lower():
                    st.write("🔐 **Permission Issue Detected**")
                    st.write("**Quick Fix:** Run in your terminal:")
                    st.code("chmod -R u+w App/db/", language="bash")
                    st.write("Then try uploading again")
                elif "Connect" in error_msg or "refused" in error_msg:
                    st.write("💡 **Fix:** Make sure Ollama is running")
                    st.write("   Run in terminal: `ollama serve`")
                elif "model" in error_msg.lower():
                    st.write("💡 **Fix:** Pull the embedding model")
                    st.write("   Run in terminal: `ollama pull mxbai-embed-large`")
                
                upload_status.update(label="Upload failed", state="error")
    
    return uploaded_files


def render_sidebar():
    """Render the sidebar with file management options."""
    from vector.vector_store import rebuild_vector_store
    
    # Initialize session state for tracking updates
    if "documents_updated" not in st.session_state:
        st.session_state.documents_updated = False
    
    with st.sidebar:
        st.header("📂 Manage Knowledge")
        
        # Display document count with dynamic update
        doc_count = count_documents()
        doc_metric = st.metric("Documents Uploaded", doc_count)
        
        # File upload section with real-time updates
        handle_file_upload()
        
        st.divider()
        
        # Button to reload the vector database
        if st.button("🔄 Refresh Knowledge Base", use_container_width=True):
            with st.status("Refreshing...", expanded=False) as status:
                try:
                    rebuild_vector_store()
                    st.cache_resource.clear()
                    st.session_state.documents_updated = True
                    st.write("✅ Knowledge base refreshed!")
                    status.update(label="Refresh complete", state="complete")
                    st.rerun()
                except Exception as e:
                    st.write(f"❌ Error: {e}")
                    status.update(label="Refresh failed", state="error")
        
        # Button to clean documents
        if st.button("🗑️ Clean Documents", use_container_width=True):
            with st.status("Cleaning...", expanded=False) as status:
                clear_documents()
                st.cache_resource.clear()
                st.session_state.documents_updated = True
                st.write("✅ All documents and knowledge base cleared!")
                status.update(label="Clean complete", state="complete")
                st.rerun()
        
        st.divider()
        
        # Button to clear chat history
        if st.button("💬 Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.cache_resource.clear()
            st.rerun()


def initialize_chat_history():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    """Display the chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_user_input():
    """Get user input from chat interface."""
    return st.chat_input("Ask a question about your documents...")


def display_user_message(question):
    """Display user message in the chat."""
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)


def get_assistant_message_placeholder():
    """Get a placeholder for the assistant message."""
    return st.chat_message("assistant"), st.empty()
