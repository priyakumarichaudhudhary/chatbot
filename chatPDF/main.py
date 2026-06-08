import os
import shutil
import pathlib
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from config import UPLOAD_DIR
from models import ChatRequest, ChatResponse
import dependencies

# Configure basic logging for the entire app
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Document Q&A API", description="AI-powered Document Q&A using LangChain")

# Serve the uploaded files statically for the PDF viewer
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    frontend_path = pathlib.Path(__file__).parent / "frontend.html"
    if frontend_path.exists():
        return frontend_path.read_text(encoding="utf-8")
    return "frontend.html not found."

@app.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    processor = dependencies.get_processor()
    if not processor:
        raise HTTPException(status_code=500, detail="Document processor not initialized due to missing API keys.")
    if not file.filename.endswith(('.pdf', '.docx', '.doc', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid file type.")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    background_tasks.add_task(processor.process_file, file_path, file.filename)
    return {"message": f"File '{file.filename}' uploaded successfully."}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    chat_svc = dependencies.get_chat_svc()
    if not chat_svc:
        raise HTTPException(status_code=500, detail="Chat service not initialized due to missing API keys.")
    return chat_svc.ask(request.session_id, request.message)
