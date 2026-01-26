# Running the Streamlit App

## Quick Start

1. **Make sure you've run ingestion first**:
   ```bash
   python3.8 -m src.ingest --docs-path /Users/iampranav/Desktop/python-3.14-docs-text
   ```

2. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to the URL shown (usually `http://localhost:8501`)

## Features

### 🎯 Interactive Query Interface
- Type any Python-related question
- Click "Search" to find relevant documentation
- Results show similarity scores and source information

### ⚙️ Customizable Settings (Sidebar)
- **Number of results**: Adjust from 1-10
- **Show detailed metadata**: Toggle source file, section, and token info
- **Show full chunk text**: View complete text or preview only

### 📊 System Information
- Total chunks in the system
- Embedding dimension
- Model information

### 💡 Example Questions
The sidebar includes suggested questions to try:
- What are Python's built-in data types?
- How do I use list comprehensions?
- Explain string slicing in Python
- How do decorators work?
- What is exception handling?
- How to read and write files?

## Understanding Results

Each result shows:
- **Similarity Score**: Percentage indicating how well the chunk matches your query (higher = better)
- **Source**: The documentation file the answer came from
- **Section**: The specific section within that file
- **Tokens**: Size of the text chunk
- **Content**: The actual documentation text

## Troubleshooting

**"RAG System Not Loaded" error**:
- Make sure `data/vector_store/` exists
- Ensure you've run ingestion successfully
- Check that `faiss_index.bin` and `chunks_metadata.json` are in the vector store directory

**App is slow to start**:
- First load downloads the embedding model (cached after first run)
- Subsequent starts are much faster

**No results or poor results**:
- Try rephrasing your question
- Be more specific or more general
- Check that your question is about Python

## Demo

You can now show:
1. The beautiful web interface
2. Real-time query and response
3. Similarity scores showing retrieval quality
4. Source attribution for transparency
5. Adjustable settings for different use cases

Perfect for demonstrating your RAG system!
