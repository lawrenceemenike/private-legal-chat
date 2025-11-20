from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.core.config import settings
from src.core.llm import get_llm

def get_rag_chain():
    """
    Constructs the RAG chain using the local LLM and ChromaDB.
    """
    # Initialize Embeddings
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
    
    # Initialize Vector Store
    db = Chroma(
        persist_directory=settings.VECTOR_STORE_DIR, 
        embedding_function=embeddings
    )
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    # Initialize LLM
    llm = get_llm()
    
    # Define Prompt Template
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep the answer concise and relevant to the legal context if applicable.

    Context: {context}

    Question: {question}

    Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )
    
    # Create Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return qa_chain
