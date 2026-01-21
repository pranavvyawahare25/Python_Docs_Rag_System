# Python Docs RAG System

A focused RAG (Retrieval-Augmented Generation) system for Python documentation that enables semantic search over Python docs.

## 🎯 Scope

This system ingests a controlled subset of Python 3.14 documentation:
- **Tutorial directory**: All tutorial files (17 files)
- **Library files**: `stdtypes.txt` and `functions.txt`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Ingestion

```bash
python src/ingest.py --docs-path /Users/iampranav/Desktop/python-3.14-docs-text
```

This will:
- Load all specified documentation files
- Chunk them semantically (preserving section structure)
- Generate embeddings using sentence-transformers
- Build FAISS vector index
- Save everything to `data/vector_store/`

### 3. Query the System

```bash
python src/query.py "How do I use list comprehensions in Python?"
```

## 📁 Project Structure

```
.
├── src/
│   ├── doc_loader.py      # Load .txt documentation files
│   ├── chunker.py          # Semantic text chunking
│   ├── embedder.py         # Generate embeddings
│   ├── vector_store.py     # FAISS vector store
│   ├── ingest.py           # Main ingestion pipeline
│   ├── query.py            # Query interface
│   ├── inspect_chunks.py   # Chunk quality inspection
│   └── utils.py            # Utility functions
├── data/
│   └── vector_store/       # Saved FAISS index and metadata
├── tests/                  # Unit tests
└── requirements.txt        # Python dependencies
```

## 🔧 How It Works

1. **Document Loading**: Loads `.txt` files from tutorial and library directories
2. **Semantic Chunking**: Splits documents by sections (headers) while maintaining context
3. **Embedding Generation**: Uses `all-MiniLM-L6-v2` sentence transformer (384-dim vectors)
4. **Vector Storage**: FAISS IndexFlatL2 for exact nearest neighbor search
5. **Retrieval**: Top-k similarity search with metadata

## 💡 Key Features

- **Structure-Aware Chunking**: Preserves document sections and hierarchy
- **Code Context Preservation**: Keeps code examples with explanations
- **Metadata Enrichment**: Tracks source file, section titles, token counts
- **Efficient Search**: FAISS-powered similarity search
- **Persistent Storage**: Save and load vector stores

## 📊 Usage Examples

### Inspect Random Chunks
```bash
python src/inspect_chunks.py --sample 10
```

### Custom Chunk Size
```bash
python src/ingest.py --docs-path /path/to/docs --chunk-size 1024
```

### Get More Results
```bash
python src/query.py "exception handling" --top-k 5
```

## 🧪 Testing

Run tests (once implemented):
```bash
pytest tests/ -v
```

## 📝 Notes

- Built for learning RAG systems with a controlled, small dataset
- Uses exact search (IndexFlatL2) - suitable for datasets up to ~100K vectors
- Embeddings are normalized for cosine similarity
- Average chunk size: ~500-600 tokens

## 🔮 Future Enhancements

- Add LLM integration for answer generation
- Implement hybrid search (BM25 + semantic)
- Add re-ranking
- Support for more document formats
- Conversation history tracking
