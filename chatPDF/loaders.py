from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_core.documents import Document
from interfaces import IDocumentLoader

class PDFLoader(IDocumentLoader):
    def load(self, file_path: str) -> List[Document]:
        return PyPDFLoader(file_path).load()

class DocxLoader(IDocumentLoader):
    def load(self, file_path: str) -> List[Document]:
        return Docx2txtLoader(file_path).load()

class TxtLoader(IDocumentLoader):
    def load(self, file_path: str) -> List[Document]:
        return TextLoader(file_path).load()

class DocumentParserRegistry:
    """Open/Closed Principle: We can add new file parsers without modifying this class."""
    def __init__(self):
        self._loaders: Dict[str, IDocumentLoader] = {}

    def register_loader(self, ext: str, loader: IDocumentLoader):
        self._loaders[ext] = loader

    def get_loader(self, ext: str) -> IDocumentLoader:
        loader = self._loaders.get(ext)
        if not loader:
            raise ValueError(f"Unsupported file format: {ext}")
        return loader
