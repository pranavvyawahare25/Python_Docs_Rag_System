"""Main ingestion pipeline for Python documentation."""

import argparse
import time
from pathlib import Path
from src.doc_loader import DocLoader
from src.chunker import SemanticChunker
from src.embedder import Embedder
from src.vector_store import VectorStore


def main():
    """Run the ingestion pipeline."""
    parser = argparse.ArgumentParser(description="Ingest Python documentation for RAG")
    parser.add_argument(
        "--docs-path",
        type=str,
        required=True,
        help="Path to Python docs directory"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/vector_store",
        help="Directory to save vector store"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=512,
        help="Target chunk size in tokens"
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence transformer model name"
    )
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    print("=" * 60)
    print("Python Documentation RAG Ingestion Pipeline")
    print("=" * 60)
    
    # Step 1: Load documents
    print("\n[1/4] Loading documents...")
    loader = DocLoader(args.docs_path)
    documents = loader.load_all_specified()
    print(f"  ✓ Loaded {len(documents)} documents")
    
    # Step 2: Chunk documents
    print("\n[2/4] Chunking documents...")
    chunker = SemanticChunker(target_chunk_size=args.chunk_size)
    chunks = chunker.chunk_documents(documents)
    print(f"  ✓ Created {len(chunks)} chunks")
    
    # Show some statistics
    token_counts = [int(c.metadata.get('token_count', 0)) for c in chunks]
    avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0
    print(f"  ✓ Average chunk size: {avg_tokens:.0f} tokens")
    
    # Step 3: Generate embeddings
    print("\n[3/4] Generating embeddings...")
    embedder = Embedder(model_name=args.model_name)
    embeddings = embedder.embed_chunks(chunks)
    print(f"  ✓ Generated {len(embeddings)} embeddings")
    print(f"  ✓ Embedding dimension: {embeddings.shape[1]}")
    
    # Step 4: Build and save vector store
    print("\n[4/4] Building vector store...")
    vector_store = VectorStore(embedding_dim=embeddings.shape[1])
    vector_store.add_chunks(chunks, embeddings)
    
    output_path = Path(args.output_dir)
    vector_store.save(str(output_path))
    print(f"  ✓ Vector store saved to {output_path}")
    
    # Summary
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("Ingestion Complete!")
    print("=" * 60)
    print(f"Documents processed: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Vector store: {output_path}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print("=" * 60)
    

if __name__ == "__main__":
    main()
