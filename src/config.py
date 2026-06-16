import os
from dotenv import load_dotenv

# Load optional environment variables from .env file
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
