import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from config import CHROMA_DB_DIR
from loaders import PDFLoader, DocxLoader, TxtLoader, DocumentParserRegistry
from vector_store import ChromaVectorStoreAdapter
from services import DocumentProcessor, RetrieverService, ChatService

logger = logging.getLogger(__name__)

# Global instances (initialized on startup)
processor: DocumentProcessor = None
retriever_svc: RetrieverService = None
chat_svc: ChatService = None

def init_dependencies():
    global processor, retriever_svc, chat_svc
    try:
        logger.info("Initializing AI dependencies...")
        embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        chroma_instance = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings_model)

        llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
        
        vector_store_adapter = ChromaVectorStoreAdapter(chroma_instance)
        
        parser_registry = DocumentParserRegistry()
        parser_registry.register_loader('pdf', PDFLoader())
        parser_registry.register_loader('docx', DocxLoader())
        parser_registry.register_loader('doc', DocxLoader())
        parser_registry.register_loader('txt', TxtLoader())

        processor = DocumentProcessor(vector_store_adapter, parser_registry)
        retriever_svc = RetrieverService(vector_store_adapter)
        chat_svc = ChatService(retriever_svc, llm)
        logger.info("Dependencies initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize AI models. Ensure API keys are set. Error: {e}", exc_info=True)
        processor = retriever_svc = chat_svc = None

def get_processor() -> DocumentProcessor:
    return processor

def get_chat_svc() -> ChatService:
    return chat_svc

init_dependencies()
