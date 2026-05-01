import streamlit as st
import os
from dotenv import load_dotenv
from agent import AdvancedRAG
import uuid

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(page_title="Ultimate Agentic RAG", page_icon="🤖", layout="wide")

st.title("🤖 Ultimate Agentic RAG Chatbot")
st.markdown("Powered by **LangGraph**, **Hybrid Search (BM25 + Vector)**, **Re-ranking**, and **Azure AI Foundry**.")

# Initialize Session State
if "rag_agent" not in st.session_state:
    st.session_state.rag_agent = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Sidebar for Config & Upload
with st.sidebar:
    st.header("⚙️ System Status")
    
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
        st.success("✅ Azure AI Foundry Configured")
    else:
        st.error("❌ Azure AI Foundry Missing in .env")
        st.info("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in the .env file.")

    st.header("📄 Document Upload")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    
    if st.button("Process Document", type="primary"):
        if uploaded_file is not None:
            with st.spinner("Executing Advanced Document Processing Pipeline..."):
                try:
                    if st.session_state.rag_agent is None:
                        st.session_state.rag_agent = AdvancedRAG()
                    
                    status = st.session_state.rag_agent.process_document(uploaded_file)
                    st.success(status)
                except Exception as e:
                    st.error(f"Error initializing RAG: {e}")
        else:
            st.warning("Please upload a file first.")
            
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        if st.session_state.rag_agent is not None:
            with st.spinner("Agentic Search & Reasoning..."):
                try:
                    response = st.session_state.rag_agent.ask(prompt, thread_id=st.session_state.thread_id)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload and process a document first from the sidebar.")
