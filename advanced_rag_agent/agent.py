import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

class AdvancedRAG:
    def __init__(self):
        # Azure AI Foundry (Azure OpenAI) Configuration
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.0
        )
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.vectorstore = None
        self.agent_executor = None
        self.memory = MemorySaver() # In-memory checkpointer for conversation states

    def process_document(self, uploaded_file) -> str:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # 1. Load Document
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(tmp_file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(tmp_file_path)
        elif ext == ".txt":
            loader = TextLoader(tmp_file_path)
        else:
            return f"Unsupported file type: {ext}"

        docs = loader.load()

        # 2. Advanced Chunking: Recursive Character with Overlap
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        splits = text_splitter.split_documents(docs)

        # 3. Vector Search (Chroma)
        # Using Chroma DB for fast, local vector storage
        self.vectorstore = Chroma.from_documents(documents=splits, embedding=self.embeddings)
        vector_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        # 4. Keyword Search (BM25)
        # BM25 is excellent for exact keyword matches, complementing dense vector search
        bm25_retriever = BM25Retriever.from_documents(splits)
        bm25_retriever.k = 5

        # 5. Hybrid Search (Ensemble)
        # Combining Vector and Keyword Search for the absolute best recall
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vector_retriever], weights=[0.3, 0.7]
        )

        # 6. Re-ranking (Flashrank)
        # Cross-encoder re-ranking to push the most relevant chunks to the very top
        compressor = FlashrankRerank(top_n=4)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=ensemble_retriever
        )

        # 7. Agentic RAG Setup (LangGraph)
        # Wrap the advanced retriever into a tool that the Agent can invoke dynamically
        tool = create_retriever_tool(
            compression_retriever,
            "document_search",
            "Search and return information from the uploaded document. Use this tool heavily when answering questions about the uploaded content."
        )
        tools = [tool]

        # Create React Agent with Memory (LangGraph is the premier agentic framework)
        self.agent_executor = create_react_agent(self.llm, tools, checkpointer=self.memory)

        # Cleanup
        os.unlink(tmp_file_path)
        
        return "Document processed successfully! Advanced Hybrid Re-ranked Index created."

    def ask(self, query: str, thread_id: str = "default") -> str:
        if not self.agent_executor:
            return "Please upload and process a document first."
        
        # Pass the thread_id to the checkpointer to maintain conversational memory
        config = {"configurable": {"thread_id": thread_id}}
        
        # Invoke the LangGraph agent
        response = self.agent_executor.invoke({"messages": [("user", query)]}, config)
        
        return response["messages"][-1].content
