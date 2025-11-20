import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Private Legal Chat"
    APP_VERSION: str = "0.1.0"
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    SOURCE_DOCS_DIR: str = os.path.join(DATA_DIR, "source_docs")
    VECTOR_STORE_DIR: str = os.path.join(DATA_DIR, "vector_store")
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    
    # LLM Settings
    # User must download a GGUF model, e.g., mistral-7b-instruct-v0.2.Q4_K_M.gguf
    MODEL_FILENAME: str = "mistral-7b-instruct-v0.2.Q4_K_M.gguf" 
    MODEL_PATH: str = os.path.join(MODELS_DIR, MODEL_FILENAME)
    
    # Model Parameters
    N_CTX: int = 4096  # Context window
    N_GPU_LAYERS: int = -1  # -1 for all layers on GPU if available, 0 for CPU only
    TEMPERATURE: float = 0.2
    
    # RAG Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    class Config:
        env_file = ".env"

settings = Settings()
