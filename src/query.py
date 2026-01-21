"""Query interface for the Python documentation RAG system."""

import argparse
from src.embedder import Embedder
from src.vector_store import VectorStore


def main():
    """Query the vector store."""
    parser = argparse.ArgumentParser(description="Query Python documentation")
    parser.add_argument(
        "query",
        type=str,
        help="Query string"
    )
    parser.add_argument(
        "--vector-store-dir",
        type=str,
        default="data/vector_store",
        help="Directory containing vector store"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of results to return"
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence transformer model name (must match ingestion)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Python Documentation RAG Query")
    print("=" * 60)
    print(f"\nQuery: {args.query}\n")
    
    # Load vector store
    print("Loading vector store...")
    vector_store = VectorStore.load(args.vector_store_dir)
    
    # Load embedder
    embedder = Embedder(model_name=args.model_name)
    
    # Embed query
    query_embedding = embedder.embed_query(args.query)
    
    # Search
    results = vector_store.search(query_embedding, k=args.top_k)
    
    # Display results
    print(f"\nTop {len(results)} results:")
    print("=" * 60)
    
    for i, (chunk, distance) in enumerate(results, 1):
        # Convert L2 distance to similarity score (inverse relationship)
        similarity = 1 / (1 + distance)
        
        print(f"\n[{i}] Similarity: {similarity:.3f} (distance: {distance:.3f})")
        print(f"Source: {chunk.metadata.get('relative_path', 'unknown')}")
        print(f"Section: {chunk.metadata.get('section_title', 'N/A')}")
        print(f"Tokens: {chunk.metadata.get('token_count', 'N/A')}")
        print(f"\nText preview (first 300 chars):")
        print("-" * 60)
        preview = chunk.text[:300] + "..." if len(chunk.text) > 300 else chunk.text
        print(preview)
        print("-" * 60)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
