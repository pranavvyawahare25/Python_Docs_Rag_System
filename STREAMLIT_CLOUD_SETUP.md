# Streamlit Cloud Deployment Guide

## Quick Setup for Streamlit Cloud

Since the `data/` folder is gitignored (contains large files), you need to upload the vector store files after deploying.

### Step 1: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your repository:
   - Repository: `pranavvyawahare25/Python_Docs_Rag_System`
   - Branch: `main`
   - Main file: `app.py`
4. Click "Deploy"

### Step 2: Upload Vector Store Files

After deployment, the app will show an upload widget because the vector store files are missing.

1. **From your local machine**, locate these files:
   ```
   data/vector_store/faiss_index.bin
   data/vector_store/chunks_metadata.json
   ```

2. **Upload both files** using the file uploader in the Streamlit app sidebar

3. Click "Load Uploaded Files"

4. The app will reload with the vector store loaded! ✅

### Alternative: Use GitHub Releases

If you want to avoid manual upload each time:

1. **Compress the vector store**:
   ```bash
   cd data
   zip -r vector_store.zip vector_store/
   ```

2. **Create a GitHub Release**:
   - Go to your repo on GitHub
   - Click "Releases" → "Create a new release"
   - Upload `vector_store.zip` as an asset
   - Publish the release

3. **Modify app.py** to download from GitHub release on first load:
   ```python
   import requests
   import zipfile
   
   def download_vector_store():
       url = "https://github.com/pranavvyawahare25/Python_Docs_Rag_System/releases/download/v1.0/vector_store.zip"
       # Download and extract logic
   ```

### File Sizes

Current vector store size:
- `faiss_index.bin`: ~434 KB
- `chunks_metadata.json`: ~923 KB
- **Total**: ~1.4 MB (within Streamlit limits)

### Troubleshooting

**Upload not working?**
- Make sure you upload BOTH files
- Check file names are exactly: `faiss_index.bin` and `chunks_metadata.json`
- Try refreshing the page

**App still showing error?**
- Clear cache: Settings → Clear cache
- Redeploy the app

**Out of resources?**
- Streamlit free tier has 1GB RAM limit
- Our app uses ~500MB, should work fine
- If issues, consider upgrading to Streamlit Cloud paid tier

## URL

Once deployed, your app will be available at:
```
https://share.streamlit.io/pranavvyawahare25/python_docs_rag_system
```

Share this URL to demonstrate your RAG system!
