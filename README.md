# PDF Chatbot Application
Python 3.12.3
A Python-based AI/ML application that enables users to upload PDF documents and interact with a chatbot that answers questions based on the document content. Built with FastAPI backend and Streamlit frontend, using LangChain and OpenAI for intelligent document processing and question-answering.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Document Upload API**: Upload PDF documents and automatically extract and process text
- **Intelligent Text Processing**: Advanced NLP techniques for text chunking and embedding generation
- **Chatbot API**: Ask questions and get AI-powered answers based on document content
- **Vector-based Search**: Uses FAISS for efficient similarity search in document embeddings
- **User-Friendly Interface**: Simple Streamlit UI for document upload and chat interaction
- **Modern LangChain Integration**: Uses latest LangChain patterns for optimal performance
- **Docker Support**: Fully containerized for easy deployment
- **RESTful API**: Well-structured API endpoints for integration

## 🏗️ Architecture

The application follows a microservices architecture with clear separation of concerns:

```
┌─────────────────┐
│  Streamlit UI   │  (Frontend - Port 8501)
│   (Frontend)    │
└────────┬────────┘
         │ HTTP Requests
         ▼
┌─────────────────┐
│  FastAPI Backend │  (API - Port 8000)
│     (API)        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ OpenAI │ │   FAISS  │
│  API   │ │  Vector  │
│        │ │   Store  │
└────────┘ └──────────┘
```

### Components

1. **Frontend (Streamlit)**: User interface for document upload and chat interaction
2. **Backend (FastAPI)**: REST API for document processing and question answering
3. **Vector Store (FAISS)**: Efficient storage and retrieval of document embeddings
4. **AI Models (OpenAI)**: Language models for embeddings and text generation

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **LangChain**: Framework for developing applications with LLMs
- **LangChain OpenAI**: OpenAI integration for LangChain
- **FAISS**: Library for efficient similarity search and clustering
- **PyPDF2**: PDF text extraction library

### Frontend
- **Streamlit**: Rapid development framework for data applications
- **Streamlit Extras**: Additional Streamlit components

### AI/ML
- **OpenAI API**: Language models for text generation and embeddings
- **LangChain Community**: Community integrations for LangChain

### Deployment
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container Docker application management

## 📦 Prerequisites

- Python 3.8 or higher (3.12 recommended)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Docker and Docker Compose (for containerized deployment)
- 2GB+ RAM recommended
- Internet connection (for OpenAI API access)

## 🚀 Installation

### Option 1: Local Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd newfolder
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env_template.txt .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   API_BASE_URL=http://localhost:8000
   ```

### Option 2: Docker Installation

See [Docker Deployment](#docker-deployment) section below.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: API Base URL (default: http://localhost:8000)
API_BASE_URL=http://localhost:8000
```

### Application Settings

The application uses the following default settings (can be modified in `api/main.py`):

- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Temperature**: 0.3 (for consistent responses)
- **Model**: gpt-3.5-turbo (can be changed to gpt-4)
- **Similarity Search**: Top 3 most relevant chunks

## 💻 Usage

### Starting the Application

#### Method 1: Using Startup Scripts

1. **Start the API server** (Terminal 1):
   ```bash
   ./start_api.sh
   ```
   The API will be available at `http://localhost:8000`

2. **Start the frontend** (Terminal 2):
   ```bash
   ./start_frontend.sh
   ```
   The UI will open at `http://localhost:8501`

#### Method 2: Manual Start

1. **Start the API:**
   ```bash
   source venv/bin/activate
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend:**
   ```bash
   source venv/bin/activate
   streamlit run frontend/app.py
   ```

### Using the Application

1. **Upload a PDF Document:**
   - Open the Streamlit UI at `http://localhost:8501`
   - Click "Choose a PDF file" and select your document
   - Click "Upload and Process"
   - Wait for processing to complete

2. **Chat with the Document:**
   - Select the uploaded document from the dropdown
   - Type your question in the chat input
   - Press Enter or click send
   - View the AI-generated answer

3. **API Usage:**
   - Access API documentation at `http://localhost:8000/docs`
   - Use the interactive API explorer to test endpoints
   - Integrate with your own applications using the REST API

## 🐳 Docker Deployment

### Quick Start with Docker Compose

1. **Create `.env` file:**
   ```bash
   cp env_template.txt .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Build and start services:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - API: `http://localhost:8000`
   - Frontend: `http://localhost:8501`
   - API Docs: `http://localhost:8000/docs`

4. **View logs:**
   ```bash
   docker-compose logs -f
   ```

5. **Stop services:**
   ```bash
   docker-compose down
   ```

### Building Individual Containers

#### Build API Container
```bash
docker build -f Dockerfile.api -t pdf-chatbot-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key pdf-chatbot-api
```

#### Build Frontend Container
```bash
docker build -f Dockerfile.frontend -t pdf-chatbot-frontend .
docker run -p 8501:8501 -e API_BASE_URL=http://api:8000 pdf-chatbot-frontend
```

### Docker Compose Services

- **api**: FastAPI backend service (port 8000)
- **frontend**: Streamlit frontend service (port 8501)
- **Volumes**: Persistent storage for uploads and vector databases
- **Network**: Internal network for service communication

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "message": "PDF Chatbot API is running",
  "version": "1.0.0"
}
```

#### 2. Upload Document
```http
POST /upload
Content-Type: multipart/form-data
```
**Request:**
- `file`: PDF file (multipart/form-data)

**Response:**
```json
{
  "document_id": "example",
  "message": "Document uploaded and processed successfully",
  "pages": 10
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

#### 3. Chat with Document
```http
POST /chat
Content-Type: application/json
```
**Request Body:**
```json
{
  "document_id": "example",
  "question": "What is the main topic of this document?"
}
```

**Response:**
```json
{
  "document_id": "example",
  "answer": "The main topic is..."
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "example",
    "question": "What is this document about?"
  }'
```

#### 4. List Documents
```http
GET /documents
```
**Response:**
```json
{
  "documents": ["doc1", "doc2", "doc3"]
}
```

#### 5. Delete Document
```http
DELETE /documents/{document_id}
```
**Response:**
```json
{
  "message": "Document 'example' deleted successfully"
}
```

### Interactive API Documentation

Access the interactive Swagger UI at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📁 Project Structure

```
newfolder/
├── api/
│   └── main.py              # FastAPI backend application
├── frontend/
│   └── app.py               # Streamlit frontend application
├── uploads/                 # Uploaded PDF files (created automatically)
├── vectorDB/                # FAISS vector stores (created automatically)
├── Dockerfile               # Main Dockerfile
├── Dockerfile.api          # API-only Dockerfile
├── Dockerfile.frontend     # Frontend-only Dockerfile
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Docker ignore file
├── requirements.txt       # Python dependencies
├── env_template.txt       # Environment variables template
├── start_api.sh           # API startup script
├── start_frontend.sh      # Frontend startup script
├── setup.py               # Dependency verification script
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🔄 How It Works

### Document Processing Pipeline

1. **Upload & Extraction:**
   - User uploads PDF through UI or API
   - Backend extracts text from all pages using PyPDF2
   - Text is validated and processed

2. **Text Chunking:**
   - Text is split into manageable chunks using RecursiveCharacterTextSplitter
   - Chunks are sized at 1000 characters with 200 character overlap
   - This ensures context preservation across chunk boundaries

3. **Embedding Generation:**
   - Each chunk is converted to vector embeddings using OpenAI's embedding model
   - Embeddings capture semantic meaning of the text
   - Vectors are stored in FAISS for efficient similarity search

4. **Vector Storage:**
   - Embeddings are stored in FAISS vector database
   - Each document has its own vector store
   - Stores are persisted to disk for future use

### Question Answering Pipeline

1. **Question Processing:**
   - User submits a question through UI or API
   - Question is processed and validated

2. **Similarity Search:**
   - Question is converted to embedding vector
   - FAISS searches for top 3 most similar document chunks
   - Relevant context is retrieved

3. **Answer Generation:**
   - Relevant chunks and question are passed to OpenAI LLM
   - LLM generates contextually relevant answer
   - Answer is returned to user

### NLP and AI Model Selection

- **Embeddings**: OpenAI's `text-embedding-ada-002` (via LangChain)
- **Language Model**: OpenAI's `gpt-3.5-turbo` (configurable to gpt-4)
- **Text Splitting**: RecursiveCharacterTextSplitter (preserves sentence boundaries)
- **Vector Search**: FAISS (fast approximate nearest neighbor search)

## 🐛 Troubleshooting

### Common Issues

#### 1. API Connection Error
**Problem**: Frontend can't connect to API
**Solution**: 
- Ensure API is running on port 8000
- Check `API_BASE_URL` in `.env` file
- Verify firewall settings

#### 2. OpenAI API Error
**Problem**: "Invalid API key" or rate limit errors
**Solution**:
- Verify `OPENAI_API_KEY` in `.env` file
- Check API key has sufficient credits
- Ensure internet connection is active

#### 3. PDF Processing Error
**Problem**: "No text could be extracted"
**Solution**:
- Ensure PDF is not password-protected
- Verify PDF contains extractable text (not just images)
- Try a different PDF file

#### 4. Import Errors
**Problem**: ModuleNotFoundError
**Solution**:
```bash
pip install -r requirements.txt
```

#### 5. Docker Issues
**Problem**: Container won't start
**Solution**:
- Check Docker is running: `docker ps`
- View logs: `docker-compose logs`
- Rebuild containers: `docker-compose build --no-cache`

### Performance Optimization

- **Large Documents**: Consider increasing chunk size for better context
- **Response Time**: Use `gpt-3.5-turbo` for faster responses
- **Accuracy**: Use `gpt-4` for better answer quality
- **Storage**: Regularly clean up old vector stores

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


