from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from src.rag.retriever import get_rag_chain
from src.rag.ingest import ingest_docs
from src.core.config import settings
import shutil
import os
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# Initialize Chain (Lazy loading recommended in production, but global for simple demo)
# Note: This might fail on startup if model is missing, so we wrap in try/except or load on request
qa_chain = None

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    result: str
    source_documents: list

@app.on_event("startup")
async def startup_event():
    global qa_chain
    try:
        if os.path.exists(settings.MODEL_PATH) and os.path.exists(settings.VECTOR_STORE_DIR):
            logger.info("Initializing RAG Chain...")
            qa_chain = get_rag_chain()
        else:
            logger.warning("Model or Vector Store not found. RAG Chain not initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Chain: {e}")

@app.get("/")
async def root():
    return {"message": "Private Legal Chat API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    global qa_chain
    if not qa_chain:
        # Try to initialize again if it failed initially (e.g. after user adds model)
        try:
            qa_chain = get_rag_chain()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"RAG Chain not initialized: {str(e)}")
            
    try:
        response = qa_chain.invoke({"query": request.query})
        
        # Format source docs
        source_docs = []
        for doc in response.get("source_documents", []):
            source_docs.append({
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 0),
                "content": doc.page_content[:200] + "..."
            })
            
        return ChatResponse(result=response["result"], source_documents=source_docs)
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def upload_and_ingest(files: list[UploadFile] = File(...)):
    """
    Uploads files to source_docs and triggers ingestion.
    """
    try:
        for file in files:
            file_path = os.path.join(settings.SOURCE_DOCS_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        # Trigger ingestion
        ingest_docs()
        
        # Reload chain to pick up new data
        global qa_chain
        qa_chain = get_rag_chain()
        
        return {"message": f"Successfully ingested {len(files)} files."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
