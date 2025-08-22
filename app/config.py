# app/config.py

# Embedding & LLM Models
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "llama3-8b-8192"

# ChromaDB Settings
CHROMA_DB_PATH = "./legal_db"
COLLECTION_NAME = "ethiopian_law"
SIMILARITY_METRIC = "cosine"
TOP_K = 5

# Chunking
CHUNK_OVERLAP = 0  # Semantic chunking only
MAX_CONTEXT_CHARS = 4000

# Environment
DATA_DIR = "data"
API_URL = "http://127.0.0.1:8000/ask"  # ✅ Now configurable