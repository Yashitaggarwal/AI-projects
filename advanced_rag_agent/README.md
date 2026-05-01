# 🤖 Ultimate Agentic RAG Chatbot

Welcome to the **Ultimate Agentic RAG Chatbot**! This project implements the most advanced, state-of-the-art techniques for Retrieval-Augmented Generation (RAG) using the industry's best agentic framework.

## 🌟 Why is this the "Best" RAG Implementation?

Building an accurate and efficient RAG system isn't just about throwing a document into a vector database. This application utilizes a meticulously designed pipeline of advanced techniques:

### 1. Document Processing & Chunking
- **Recursive Character Text Splitting:** We chunk documents intelligently, respecting paragraph and sentence boundaries.
- **Overlapping:** We use a `chunk_size` of 1000 with a `chunk_overlap` of 200. This ensures that context isn't lost if an important concept spans across the boundary of a chunk.

### 2. Hybrid Search (The Ultimate Retrieval Setup)
Instead of relying purely on vector embeddings (which sometimes miss exact keyword matches like part numbers or specific names), we use an **Ensemble Retriever**:
- **Dense Retrieval (Chroma DB):** Understands the semantic meaning and context of the query.
- **Sparse Retrieval (BM25):** Acts as a traditional keyword search engine for exact term matching.
- **Ensemble Combination:** We weight these results (e.g., 70% Vector, 30% BM25) to get the absolute best candidate chunks.

### 3. Re-ranking (Contextual Compression)
Fetching 10-15 chunks from a vector database introduces "noise" to the LLM. 
- We use **Flashrank** (a lightweight, ultra-fast Cross-Encoder) to re-evaluate and re-rank the candidate chunks against the user's query.
- This ensures only the top 4 *most relevant* chunks are passed to the LLM, dramatically improving accuracy and reducing token usage/memory.

### 4. Agentic Framework (LangGraph)
We don't just use a simple chain. We use **LangGraph**—currently the world's leading framework for building stateful, multi-actor LLM agents.
- **Tool Use:** The RAG pipeline is provided as a tool to a ReAct (Reasoning + Acting) Agent. The Agent decides *if* it needs to search the document, *what* query to search for, and can search multiple times if the first answer isn't sufficient.
- **Memory/Checkpointer:** LangGraph's checkpointer is used to maintain conversation history across a thread, allowing for perfect multi-turn conversations.

### 5. Azure AI Foundry Integration
- Ready to plug into enterprise-grade **Azure OpenAI** endpoints for both Text Embeddings and Large Language Models.

---

## 🚀 How to Run

1. **Install Dependencies:**
   Navigate to this directory and install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Edit the `.env` file and insert your Azure AI Foundry credentials:
   ```env
   AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
   AZURE_OPENAI_API_KEY="your-api-key"
   AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-ada-002"
   AZURE_OPENAI_API_VERSION="2024-02-15-preview"
   ```

3. **Run the Streamlit UI:**
   ```bash
   streamlit run app.py
   ```

4. **Use the App:**
   - Upload a PDF, DOCX, or TXT file via the sidebar.
   - Click "Process Document" to build the Hybrid Re-ranked Index.
   - Start chatting! The agent remembers context across the conversation.

## 🛠️ Tech Stack Justification
- **Streamlit:** Best-in-class for rapidly building highly interactive, beautiful ML/AI UIs.
- **LangChain / LangGraph:** LangGraph is specifically chosen because it provides cyclic graph execution, meaning the agent can loop its reasoning and tool-calling capabilities reliably, far outperforming standard linear chains.
- **Chroma DB:** An excellent, fast, local vector database that doesn't require a heavy separate server setup (like Qdrant or Pinecone) for local testing, while maintaining high performance.
- **Flashrank:** Chosen over Cohere Re-rank to avoid needing an extra API key, while still providing state-of-the-art cross-encoder re-ranking locally.
