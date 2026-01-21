# Troubleshooting File Upload on Streamlit Cloud

## Issue: "Load Uploaded Files" Not Working

If the upload isn't working, try these steps in order:

### Step 1: Verify File Names
Make sure your files are named EXACTLY:
- `faiss_index.bin` (NOT `faiss_index.bin.bin` or any other variation)
- `chunks_metadata.json` (NOT `chunks_metadata.json.txt`)

**How to check on Mac:**
- Right-click file → Get Info
- Look at "Name & Extension"
- Make sure "Hide extension" is unchecked

### Step 2: Upload Both Files Together
1. Click "Browse files"
2. Select BOTH files at once (Cmd+Click or Shift+Click)
3. You should see both files listed with their sizes
4. The button will only appear if both required files are selected

### Step 3: Check File Sizes
Expected sizes (approximately):
- `faiss_index.bin`: ~400-500 KB
- `chunks_metadata.json`: ~900-1000 KB

If your files are much smaller or larger, they might be corrupted.

### Step 4: Try Fresh Upload
1. Refresh the Streamlit app page (Cmd+R or F5)
2. Upload the files again
3. Wait for both files to fully upload (you'll see file sizes)
4. Click "Load Uploaded Files"

### Step 5: Check Browser Console
If still not working:
1. Open browser developer tools (F12 or Cmd+Option+I)
2. Go to Console tab
3. Look for any error messages
4. Share the error with me

### Step 6: Alternative - Use Local Files

If cloud upload keeps failing, you can:

1. **Clone the repo locally**:
   ```bash
   git clone https://github.com/pranavvyawahare25/Python_Docs_Rag_System.git
   cd Python_Docs_Rag_System
   ```

2. **Copy your vector store**:
   ```bash
   mkdir -p data/vector_store
   cp /path/to/your/data/vector_store/* data/vector_store/
   ```

3. **Run locally**:
   ```bash
   streamlit run app.py
   ```

## Common Issues

### "File not found" after upload
- The app cache might not have cleared
- Try: Settings (⋮) → Clear cache → Rerun

### "Invalid file type"
- Make sure you're uploading .bin and .json files
- Not .zip or compressed files

### "Out of memory"
- Vector store too large for free tier
- Streamlit free tier: 1GB RAM limit
- Our files should fit (~1.4 MB total)

### Button doesn't appear
- Both files must be selected
- File names must match exactly
- Check that file types are correct (.bin and .json)

## Still Having Issues?

Let me know:
1. What error message you see (exact text)
2. File sizes of your uploads
3. Screenshot of the upload interface
4. Any console errors

I'll help you debug further!
