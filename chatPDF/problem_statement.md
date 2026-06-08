Role: You are a Senior AI Solutions Architect, LangChain Expert, and Full-Stack Engineer.

Objective

Design and implement a scalable AI-powered Document Q&A application that enables users to upload PDF/DOCX/TXT files and ask natural-language questions about the uploaded content.

The solution must follow modern software engineering practices, SOLID principles, clean architecture, and production-grade system design.

Functional Requirements
1. Document Upload
Support:
PDF
DOCX
TXT
Validate file type and size.
Store uploaded files securely.
2. Document Processing
Extract text from uploaded files.
Clean and normalize content.
Chunk documents using an optimal chunking strategy.
Generate embeddings for each chunk.
Store embeddings in a vector database.
3. Retrieval-Augmented Generation (RAG)

Use:

LangChain
Embedding Model
Vector Database
Semantic Search

Recommended flow:

Upload Document
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Database
      ↓
Retriever
      ↓
LLM
      ↓
Conversational Answer
4. Question Answering

Users can ask questions related to uploaded documents.

The system should:

Retrieve only relevant chunks.
Generate answers using retrieved context.
Cite source passages and page numbers when available.
Maintain conversational chat history.
5. Out-of-Context Protection

If sufficient evidence is not found in retrieved content:

Respond with:

"I couldn't find information related to that question in the uploaded document."

Requirements:

No hallucinations.
No external knowledge.
Confidence threshold validation.
Retrieval relevance scoring.
6. Conversational Responses

Responses should:

Be natural and conversational.
Summarize information clearly.
Include supporting references.
Preserve chat context.
Technical Requirements
AI Stack
LangChain
OpenAI Embeddings (or equivalent)
OpenAI GPT model (or equivalent)
RAG Architecture
Vector Database

Choose one:

ChromaDB
Pinecone
Weaviate
FAISS

Explain pros and cons.

System Design
High-Level Design (HLD)

Provide:

Components
Frontend
API Layer
Document Service
Embedding Service
Vector Store
Retrieval Service
LLM Service
Chat Service
Architecture Diagram

Create a detailed architecture diagram showing:

Frontend
   ↓
Backend API
   ↓
Document Processing Service
   ↓
Embedding Service
   ↓
Vector DB
   ↓
Retriever
   ↓
LLM
   ↓
Response
Low-Level Design (LLD)

Apply SOLID principles.

Design classes/modules such as:

DocumentUploader
DocumentParser
ChunkingService
EmbeddingService
VectorStoreRepository
RetrieverService
ChatService
PromptBuilder
ResponseGenerator
ConversationManager

For each class provide:

Responsibility
Methods
Interfaces
Dependency relationships
Non-Functional Requirements
Performance
Support large PDFs (500+ pages)
Fast retrieval
Efficient embedding generation
Scalability
Multiple users
Multi-document support
Session management
Security
File validation
Access control
Secure API design
Reliability
Error handling
Retry mechanisms
Logging and monitoring
UI Requirements

Create a simple and intuitive UI.

Layout

Left Panel

Upload Document
Document List

Right Panel

Chat Interface
Features
Drag-and-drop upload
Chat history
Typing indicator
Source references
Responsive design

Provide wireframe mockups.