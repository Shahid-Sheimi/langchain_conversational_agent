"""
Streamlit Frontend for PDF Chatbot Application
Provides user interface for document upload and chat interaction
"""

import streamlit as st
import requests
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page Configuration
st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="💬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    #MainMenu {
        visibility: hidden;
    }
    .stDeployButton {
        display: none;
    }
    footer {
        visibility: hidden;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""

""", unsafe_allow_html=True)

st.title("Chat with PDF 💬")

# Sidebar
with st.sidebar:
    st.title('🤗💬 PDF Chat App')
    st.markdown('''
    ## About
    
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [FastAPI](https://fastapi.tiangolo.com/)
    - [LangChain](https://python.langchain.com/)
    - [FAISS](https://ai.meta.com/tools/faiss/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
    
    ## API Endpoints
    - **POST /upload**: Upload PDF documents
    - **POST /chat**: Ask questions about documents
    - **GET /documents**: List all documents
    - **DELETE /clear-all**: Clear all uploaded data
    ''')
    add_vertical_space(5)
    
    # API Status Check
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Connection Failed")
    except:
        st.error("❌ API Not Available")
        st.info(f"Make sure the API is running at {API_BASE_URL}")


def upload_document(file):
    """Upload PDF document to API"""
    try:
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def chat_with_document(document_id, question):
    """Send chat question to API"""
    try:
        payload = {
            "document_id": document_id,
            "question": question
        }
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.json().get('detail', 'Unknown error')
            st.error(f"Chat failed: {error_msg}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def get_documents():
    """Get list of uploaded documents"""
    try:
        response = requests.get(f"{API_BASE_URL}/documents", timeout=5)
        if response.status_code == 200:
            return response.json().get("documents", [])
        return []
    except:
        return []


def clear_all_data():
    """Clear all uploaded data from API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/clear-all", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.json().get('detail', 'Unknown error')
            st.error(f"Clear failed: {error_msg}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    if "current_document" not in st.session_state:
        st.session_state.current_document = None
    
    # Document Upload Section
    st.header("📄 Upload PDF Document")
    pdf = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")
    
    if pdf is not None:
        if st.button("Upload and Process", type="primary"):
            with st.spinner("Uploading and processing document..."):
                result = upload_document(pdf)
                if result:
                    st.session_state.current_document = result["document_id"]
                    st.success(f"✅ {result['message']}")
                    st.info(f"📄 Document ID: {result['document_id']} | Pages: {result['pages']}")
                    # Initialize chat history for this document
                    if result["document_id"] not in st.session_state.messages:
                        st.session_state.messages[result["document_id"]] = []
    
    # Document Selection
    st.divider()
    st.header("📚 Select Document")
    
    documents = get_documents()
    
    # Clear All Data Button
    col1, col2 = st.columns([3, 1])
    with col1:
        if documents:
            selected_doc = st.selectbox(
                "Choose a document to chat with:",
                options=documents,
                index=0 if st.session_state.current_document in documents 
                      else documents.index(documents[0]) if documents else 0,
                key="doc_selector"
            )
            st.session_state.current_document = selected_doc
            
            # Initialize chat history if needed
            if selected_doc not in st.session_state.messages:
                st.session_state.messages[selected_doc] = []
        else:
            st.info("No documents uploaded yet. Please upload a PDF document first.")
            selected_doc = None
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        clear_button = st.button("🗑️ Clear All Data", type="secondary", use_container_width=True)
        
        if clear_button:
            if st.session_state.get("confirm_clear", False):
                # Second click - actually clear
                with st.spinner("Clearing all uploaded data..."):
                    result = clear_all_data()
                    if result:
                        st.success(f"✅ {result['message']}")
                        st.info(f"🗑️ Deleted {result['deleted_files']} files and {result['deleted_vector_stores']} vector stores")
                        # Clear session state
                        st.session_state.messages = {}
                        st.session_state.current_document = None
                        st.session_state.confirm_clear = False
                        st.rerun()
            else:
                # First click - show confirmation
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click 'Clear All Data' again to confirm deletion of all uploaded files and vector databases")
        
        # Show confirmation status
        if st.session_state.get("confirm_clear", False):
            st.caption("⚠️ Confirmation pending...")
    
    # Chat Interface
    if selected_doc:
        st.divider()
        st.header("💬 Chat with Document")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages[selected_doc]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # Chat input
        query = st.chat_input("Ask questions about the PDF file:")
        
        if query:
            # Add user message to chat
            st.session_state.messages[selected_doc].append({
                "role": "user",
                "content": query
            })
            
            with st.chat_message("user"):
                st.write(query)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = chat_with_document(selected_doc, query)
                    if result:
                        answer = result["answer"]
                        st.write(answer)
                        # Add bot message to chat
                        st.session_state.messages[selected_doc].append({
                            "role": "assistant",
                            "content": answer
                        })
                    else:
                        st.error("Failed to get response from the chatbot.")


if __name__ == "__main__":
    main()

