# Deployment Guide for Streamlit App

This guide explains how to run and deploy the Python Docs RAG Streamlit application.

## Local Development

### Run Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Requirements

Make sure the vector store is created first:
```bash
python3.8 -m src.ingest --docs-path /Users/iampranav/Desktop/python-3.14-docs-text
```

## Streamlit Cloud Deployment

### Prerequisites

1. Push your code to GitHub (already done!)
2. Ensure `data/` is in `.gitignore` (it is!)
3. Have a Streamlit Cloud account

### Deployment Steps

1. **Go to**: https://share.streamlit.io/

2. **New app** → Connect your GitHub repository:
   - Repository: `pranavvyawahare25/Python_Docs_Rag_System`
   - Branch: `main`
   - Main file path: `app.py`

3. **Important**: You'll need to upload the vector store data

   Since the `data/` folder is gitignored, you have two options:

   **Option A: Upload as GitHub Release Asset**
   - Create a GitHub release
   - Attach `data.zip` (compress data/vector_store/)
   - Modify `app.py` to download on first run

   **Option B: Use Streamlit Secrets**
   - Use a cloud storage service (S3, Google Drive, etc.)
   - Store the vector store files there
   - Load from cloud in the app

### Quick Fix for Deployment

Since the vector store is large, here's the easiest approach:

**Generate smaller test vector store on Streamlit Cloud**:

1. Upload just a few sample text files
2. Run ingestion on the cloud
3. Or use a pre-generated mini vector store

## Docker Deployment (Alternative)

Create a `Dockerfile`:

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run ingestion (if needed)
# RUN python -m src.ingest --docs-path /docs

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t python-docs-rag .
docker run -p 8501:8501 python-docs-rag
```

## Environment Variables

Set these if using cloud storage for data:

```bash
export VECTOR_STORE_PATH="path/to/vector_store"
export EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
```

## Troubleshooting

**Issue**: "RAG System Not Loaded"
- **Solution**: Ensure `data/vector_store/` exists with `faiss_index.bin` and `chunks_metadata.json`

**Issue**: Model download slow
- **Solution**: First load caches the model. Subsequent loads are faster.

**Issue**: Out of memory on free Streamlit Cloud
- **Solution**: Use a smaller embedding model or reduce chunk count
