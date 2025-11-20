# Private Legal Chat (LLMOps Demo)

A secure, local-first RAG (Retrieval-Augmented Generation) chat application designed for confidential legal documents. This system runs entirely offline using local LLMs (Mistral 7B / Llama 2) and a local vector database, ensuring no data leaves your infrastructure.

## Architecture

```mermaid
graph TD
    User[User] --> UI[Streamlit UI]
    UI --> API[FastAPI Backend]
    API --> Chain[RAG Chain]
    Chain --> Retriever[Retriever]
    Retriever --> VectorDB[(ChromaDB)]
    Chain --> LLM[Local LLM (LlamaCpp)]
    
    subgraph "Ingestion Pipeline"
        Docs[PDF/TXT Docs] --> Loader[Document Loader]
        Loader --> Splitter[Text Splitter]
        Splitter --> Embeddings[HuggingFace Embeddings]
        Embeddings --> VectorDB
    end
```

## Features
- **Privacy First**: Runs 100% locally. No external API calls (OpenAI, etc.).
- **RAG Pipeline**: Ingests PDF and TXT files, creates embeddings, and retrieves relevant context.
- **Interactive UI**: Streamlit-based chat interface with source citation.
- **API Layer**: FastAPI backend for extensibility.
- **Containerized**: Docker support for easy deployment.

## Prerequisites
- Docker & Docker Compose
- **OR** Python 3.10+
- **Model Weights**: You must download a GGUF formatted model.

## Setup Instructions

### 1. Download Model
Due to size constraints, the model is not included in the repo.
1.  Download **Mistral-7B-Instruct-v0.2.Q4_K_M.gguf** (approx 4GB) or similar from HuggingFace (TheBloke/Mistral-7B-Instruct-v0.2-GGUF).
2.  Place the file in the `models/` directory.
3.  Rename it to `mistral-7b-instruct-v0.2.Q4_K_M.gguf` or update `src/core/config.py`.

### 2. Run with Docker (Recommended)
```bash
docker-compose up --build
```
- **UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

### 3. Run Locally (Manual)
1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: For GPU support with `llama-cpp-python`, refer to their [installation guide](https://github.com/abetlen/llama-cpp-python) for specific flags.*

3.  Run the API:
    ```bash
    uvicorn src.api.main:app --reload
    ```
4.  Run the UI (in a separate terminal):
    ```bash
    streamlit run src/ui/app.py
    ```

## Usage
1.  Open the UI at `http://localhost:8501`.
2.  Use the sidebar to upload legal PDF documents.
3.  Click "Ingest Documents".
4.  Start chatting! The system will answer based on the uploaded context.

## Project Structure
- `src/api`: FastAPI backend.
- `src/core`: Configuration and LLM initialization.
- `src/rag`: Ingestion and Retrieval logic.
- `src/ui`: Streamlit frontend.
- `data/`: Stores uploaded docs and vector database.
- `models/`: Stores the GGUF model file.
