import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

UPLOAD_DIR = "./uploads"
CHROMA_DB_DIR = "./chroma_db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
