---
title: PDF Chatbot
emoji: 💬
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# PDF Chatbot on Hugging Face Spaces

A PDF chatbot application that allows users to upload PDF documents and interact with an AI-powered chatbot that answers questions based on document content.

## 🚀 Quick Start

1. **Fork this Space** or create a new Docker Space on Hugging Face
2. **Add your OpenAI API Key** as a Secret:
   - Go to Space Settings → Variables and Secrets
   - Add a new Secret: `OPENAI_API_KEY` with your API key value
3. **The Space will automatically build and deploy**

## 📋 Prerequisites

- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- Hugging Face account

## 🔧 Configuration

### Environment Variables

Set these in your Space Settings → Variables and Secrets:

- `OPENAI_API_KEY` (Required): Your OpenAI API key
- `API_BASE_URL` (Optional): Defaults to `http://localhost:8000` for containerized deployment

## 📁 Project Structure

```
.
├── Dockerfile.hf          # Dockerfile for Hugging Face Spaces
├── start_hf.sh           # Startup script that runs both services
├── api/
│   └── main.py          # FastAPI backend
├── frontend/
│   └── app.py           # Streamlit frontend
└── requirements.txt     # Python dependencies
```

## 🏗️ Architecture

This deployment runs both services in a single container:

- **FastAPI Backend**: Runs on port 8000 (internal)
- **Streamlit Frontend**: Runs on port 7860 (exposed to users)

The frontend communicates with the backend API via `localhost:8000` within the container.

## 📚 Features

- Upload PDF documents
- Automatic text extraction and processing
- Vector-based similarity search using FAISS
- AI-powered question answering using OpenAI LLM
- Clean, intuitive Streamlit interface

## 🛠️ Local Development

For local development, you can still use the original setup:

```bash
# Using docker-compose
docker-compose up -d

# Or using individual scripts
./start_api.sh    # Terminal 1
./start_frontend.sh  # Terminal 2
```

## 📖 Usage

1. Upload a PDF document using the file uploader
2. Wait for processing to complete
3. Select the document from the dropdown
4. Ask questions about the document content
5. Get AI-powered answers based on the document

## 🔍 API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - Health check
- `POST /upload` - Upload PDF document
- `POST /chat` - Ask questions about documents
- `GET /documents` - List all uploaded documents
- `DELETE /documents/{document_id}` - Delete a document
- `DELETE /clear-all` - Clear all uploaded data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

