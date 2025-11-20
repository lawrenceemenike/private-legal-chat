import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.core.config import settings

def load_documents() -> List:
    """
    Loads PDF and Text documents from the source directory.
    """
    documents = []
    
    # Load PDFs
    if os.path.exists(settings.SOURCE_DOCS_DIR):
        pdf_loader = DirectoryLoader(
            settings.SOURCE_DOCS_DIR,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents.extend(pdf_loader.load())
        
        # Load Text files
        txt_loader = DirectoryLoader(
            settings.SOURCE_DOCS_DIR,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents.extend(txt_loader.load())
    
    return documents

def ingest_docs():
    """
    Main ingestion function: loads docs, splits them, and saves to Vector DB.
    """
    print(f"Loading documents from {settings.SOURCE_DOCS_DIR}...")
    documents = load_documents()
    
    if not documents:
        print("No documents found. Please add PDF or TXT files to data/source_docs/")
        return

    print(f"Loaded {len(documents)} documents.")
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")
    
    # Create Embeddings
    print(f"Creating embeddings using {settings.EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
    
    # Create/Update Vector Store
    print(f"Persisting to ChromaDB at {settings.VECTOR_STORE_DIR}...")
    db = Chroma.from_documents(
        texts, 
        embeddings, 
        persist_directory=settings.VECTOR_STORE_DIR
    )
    db.persist()
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_docs()
