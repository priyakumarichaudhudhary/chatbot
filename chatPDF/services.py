import logging
from typing import List, Dict, Any
from fastapi import HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document
from langchain_groq import ChatGroq

from interfaces import IVectorStore
from loaders import DocumentParserRegistry

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, vector_store: IVectorStore, parser_registry: DocumentParserRegistry):
        self.vector_store = vector_store
        self.parser_registry = parser_registry
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def process_file(self, file_path: str, filename: str):
        try:
            ext = filename.split('.')[-1].lower()
            loader = self.parser_registry.get_loader(ext)
            docs = loader.load(file_path)
            
            for doc in docs:
                doc.metadata["source"] = filename

            splits = self.text_splitter.split_documents(docs)
            self.vector_store.add_documents(splits)
            logger.info(f"Successfully processed {filename}.")
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}", exc_info=True)

class RetrieverService:
    def __init__(self, vector_store: IVectorStore, threshold: float = 0.0, top_k: int = 4):
        self.vector_store = vector_store
        self.threshold = threshold
        self.top_k = top_k
        
    def retrieve(self, query: str) -> List[Document]:
        try:
            results = self.vector_store.similarity_search_with_relevance_scores(query, k=self.top_k)
            # Remove strict threshold filtering so the LLM always sees the top K chunks.
            # The system prompt handles ignoring irrelevant chunks.
            return [doc for doc, score in results]
        except Exception as e:
            logger.error(f"Error during retrieval: {e}", exc_info=True)
            if "401" in str(e):
                raise HTTPException(status_code=401, detail="Authentication failed. Check your API key.")
            raise

class ChatService:
    def __init__(self, retriever_service: RetrieverService, llm: ChatGroq):
        self.retriever_service = retriever_service
        self.llm = llm
        self.chat_histories: Dict[str, List[Any]] = {}
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful, intelligent AI assistant, similar to ChatGPT. You have vast general knowledge and can chat about any topic. Additionally, you may be provided with specific document context. If the user asks a question related to the provided documents, use the context to answer and include source citations (e.g., document name). If the user asks a general question, ignore the document context (unless relevant) and answer normally using your general knowledge. If the user specifically asks about the documents but the context doesn't contain the answer, state that the information isn't in the uploaded documents.\n\nContext: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])

    def ask(self, session_id: str, query: str) -> Dict[str, Any]:
        try:
            docs = self.retriever_service.retrieve(query)

            context = "\n\n".join([f"[Source: {d.metadata.get('source', 'Unknown')}, Page: {d.metadata.get('page', 'Unknown')}]\n{d.page_content}" for d in docs])
            
            if session_id not in self.chat_histories:
                self.chat_histories[session_id] = []
            history = self.chat_histories[session_id]

            chain = self.prompt | self.llm | StrOutputParser()
            answer = chain.invoke({"context": context, "chat_history": history, "input": query})
            
            history.extend([HumanMessage(content=query), AIMessage(content=answer)])
            if len(history) > 10:
                 self.chat_histories[session_id] = history[-10:]

            sources = [{"source": d.metadata.get("source"), "page": d.metadata.get("page", 0), "content": d.page_content[:200]+"..."} for d in docs]
            return {"answer": answer, "sources": sources}
            
        except Exception as e:
            logger.error(f"Error during chat generation: {e}", exc_info=True)
            if "401" in str(e):
                raise HTTPException(status_code=401, detail="Authentication error: Please verify your API key in the .env file.")
            raise HTTPException(status_code=500, detail=str(e))
