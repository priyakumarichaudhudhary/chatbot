from abc import ABC, abstractmethod
from typing import List, Tuple
from langchain_core.documents import Document

class IDocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> List[Document]:
        pass

class IVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]):
        pass
    
    @abstractmethod
    def similarity_search_with_relevance_scores(self, query: str, k: int) -> List[Tuple[Document, float]]:
        pass
