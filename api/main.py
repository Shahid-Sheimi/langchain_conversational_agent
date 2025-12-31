"""
FastAPI Backend for PDF Chatbot Application

This module provides a RESTful API for uploading PDF documents and interacting
with a chatbot that answers questions based on document content.

Key Features:
- Document upload and text extraction
- Vector embedding generation using OpenAI
- FAISS-based similarity search
- Question-answering using LangChain and OpenAI LLM
- Support for both modern and legacy LangChain APIs

Author: Soumya
License: Educational/Demonstration purposes
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from pathlib import Path

from PyPDF2 import PdfReader

# Text splitter - try newer location first
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

# Embeddings and LLM - prefer langchain_openai for newer versions
USE_CHAT_OPENAI = False
try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    USE_CHAT_OPENAI = True
except ImportError:
    try:
        from langchain_community.embeddings.openai import OpenAIEmbeddings
        from langchain_community.llms import OpenAI
    except ImportError:
        from langchain.embeddings.openai import OpenAIEmbeddings
        from langchain_community.llms import OpenAI

from langchain_community.vectorstores import FAISS

# QA Chain - try modern approach first, fallback to deprecated methods
USE_MODERN_CHAIN = False
try:
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate
    USE_MODERN_CHAIN = True
except ImportError:
    try:
        from langchain_classic.chains.question_answering import load_qa_chain
    except ImportError:
        try:
            from langchain.chains.question_answering import load_qa_chain
        except ImportError:
            try:
                from langchain.chains.qa import load_qa_chain
            except ImportError:
                try:
                    from langchain.chains import load_qa_chain
                except ImportError:
                    # Fallback: create a simple QA function
                    def load_qa_chain(llm, chain_type="stuff"):
                        class SimpleQAChain:
                            def __init__(self, llm):
                                self.llm = llm                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                            def run(self, input_documents, question):
                                context = "\n".join([doc.page_content for doc in input_documents])
                                prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
                                return self.llm(prompt)
                        return SimpleQAChain(llm)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="PDF Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
VECTORDB_DIR = Path("vectorDB")
UPLOAD_DIR.mkdir(exist_ok=True)
VECTORDB_DIR.mkdir(exist_ok=True)


# Request/Response Models
class ChatRequest(BaseModel):
    document_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str
    document_id: str


class UploadResponse(BaseModel):
    document_id: str
    message: str
    pages: int


# Global variables for embeddings and text splitter
# These are initialized once and reused across requests for efficiency
embeddings = OpenAIEmbeddings()  # OpenAI embedding model for vector generation
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Maximum characters per chunk
    chunk_overlap=200,    # Overlap between chunks to preserve context
    length_function=len   # Function to calculate text length
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "PDF Chatbot API is running", "version": "1.0.0"}


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Document Upload API Endpoint
    
    Processes uploaded PDF files by:
    1. Extracting text from all pages
    2. Splitting text into manageable chunks
    3. Generating vector embeddings for each chunk
    4. Storing embeddings in FAISS vector database
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        UploadResponse: Document ID, success message, and page count
        
    Raises:
        HTTPException: If file is not PDF or processing fails
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file to local storage
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from all PDF pages
        pdf_reader = PdfReader(file_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Validate that text was extracted
        if not text.strip():
            raise HTTPException(
                status_code=400, 
                detail="No text could be extracted from the PDF. Ensure the PDF contains extractable text."
            )
        
        # Split text into chunks for efficient processing
        # Chunks preserve context with overlap to maintain semantic meaning
        chunks = text_splitter.split_text(text)
        
        # Create document ID from filename (remove .pdf extension)
        document_id = file.filename[:-4] if file.filename.endswith('.pdf') else file.filename
        
        # Create or update vector store
        vectordb_path = VECTORDB_DIR / document_id
        if vectordb_path.exists():
            # Document already exists - load and update with new chunks
            vectordb = FAISS.load_local(
                str(vectordb_path), 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            # Add new chunks to existing vector store
            vectordb.add_texts(chunks)
        else:
            # New document - create vector store from chunks
            vectordb = FAISS.from_texts(chunks, embeddings)
        
        # Persist vector store to disk for future use
        vectordb.save_local(str(vectordb_path))
        
        return UploadResponse(
            document_id=document_id,
            message="Document uploaded and processed successfully",
            pages=len(pdf_reader.pages)
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    """
    Chatbot API Endpoint
    
    Processes user questions by:
    1. Loading the document's vector store
    2. Finding most relevant document chunks using similarity search
    3. Generating contextually relevant answers using OpenAI LLM
    
    Args:
        request: ChatRequest containing document_id and question
        
    Returns:
        ChatResponse: Document ID and AI-generated answer
        
    Raises:
        HTTPException: If document not found or answer generation fails
    """
    try:
        # Load vector store for the requested document
        vectordb_path = VECTORDB_DIR / request.document_id
        
        # Validate document exists
        if not vectordb_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"Document '{request.document_id}' not found. Please upload it first."
            )
        
        # Load FAISS vector database from disk
        vectordb = FAISS.load_local(
            str(vectordb_path),
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Perform similarity search to find most relevant document chunks
        # k=3 retrieves top 3 most similar chunks for context
        docs = vectordb.similarity_search(request.question, k=3)
        
        # Handle case where no relevant chunks found
        if not docs:
            return ChatResponse(
                document_id=request.document_id,
                answer="I couldn't find relevant information in the document to answer your question."
            )
        
        # Initialize Language Model
        # Use modern ChatOpenAI if available, otherwise fallback to legacy OpenAI
        if USE_CHAT_OPENAI:
            # ChatOpenAI implements Runnable interface required by modern chains
            llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
        else:
            # Legacy OpenAI LLM for older LangChain versions
            llm = OpenAI(temperature=0.3)
        
        # Generate answer using appropriate chain approach
        if USE_MODERN_CHAIN:
            # Modern LangChain approach (recommended)
            # Uses create_stuff_documents_chain for better performance
            prompt = ChatPromptTemplate.from_template(
                """Use the following pieces of context to answer the question at the end.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.

                Context: {context}

                Question: {input}
                
                Answer:"""
            )
            chain = create_stuff_documents_chain(llm, prompt)
            result = chain.invoke({"context": docs, "input": request.question})
            # Handle different response formats
            if isinstance(result, dict):
                response = result.get("output_text", result.get("answer", str(result)))
            else:
                response = str(result)
        else:
            # Fallback to deprecated load_qa_chain for older versions
            chain = load_qa_chain(llm, chain_type="stuff")
            # Try modern invoke method first, fallback to deprecated run method
            if hasattr(chain, 'invoke'):
                response = chain.invoke({"input_documents": docs, "question": request.question})
                if isinstance(response, dict):
                    response = response.get("output_text", str(response))
            else:
                response = chain.run(input_documents=docs, question=request.question)
        
        return ChatResponse(
            document_id=request.document_id,
            answer=response
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions (validation/not found errors)
        raise
    except Exception as e:
        # Handle unexpected errors during answer generation
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    documents = []
    for path in VECTORDB_DIR.iterdir():
        if path.is_dir():
            documents.append(path.name)
    return {"documents": documents}


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its vector store"""
    vectordb_path = VECTORDB_DIR / document_id
    if vectordb_path.exists():
        shutil.rmtree(vectordb_path)
        return {"message": f"Document '{document_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")


@app.delete("/clear-all")
async def clear_all_data():
    """
    Clear all uploaded data including PDFs and vector databases
    
    This endpoint removes:
    - All uploaded PDF files from uploads/ directory
    - All vector databases from vectorDB/ directory
    
    Returns:
        Success message with count of deleted items
    """
    try:
        deleted_files = 0
        deleted_vectors = 0
        
        # Clear all uploaded PDF files
        if UPLOAD_DIR.exists():
            for file_path in UPLOAD_DIR.iterdir():
                if file_path.is_file():
                    file_path.unlink()
                    deleted_files += 1
        
        # Clear all vector databases
        if VECTORDB_DIR.exists():
            for vectordb_path in VECTORDB_DIR.iterdir():
                if vectordb_path.is_dir():
                    shutil.rmtree(vectordb_path)
                    deleted_vectors += 1
        
        return {
            "message": "All uploaded data cleared successfully",
            "deleted_files": deleted_files,
            "deleted_vector_stores": deleted_vectors
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

