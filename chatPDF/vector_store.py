from typing import List, Tuple
from langchain_chroma import Chroma
from langchain_core.documents import Document
from interfaces import IVectorStore

class ChromaVectorStoreAdapter(IVectorStore):
    """Adapter pattern to decouple Chroma implementation details."""
    def __init__(self, chroma_instance: Chroma):
        self._chroma = chroma_instance

    def add_documents(self, documents: List[Document]):
        self._chroma.add_documents(documents)
        
    def similarity_search_with_relevance_scores(self, query: str, k: int) -> List[Tuple[Document, float]]:
        return self._chroma.similarity_search_with_relevance_scores(query, k=k)
