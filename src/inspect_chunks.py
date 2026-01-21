"""Inspect chunks to verify quality."""

import argparse
import random
from src.vector_store import VectorStore


def main():
    """Inspect random chunks from the vector store."""
    parser = argparse.ArgumentParser(description="Inspect chunk quality")
    parser.add_argument(
        "--vector-store-dir",
        type=str,
        default="data/vector_store",
        help="Directory containing vector store"
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=5,
        help="Number of random chunks to display"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Chunk Quality Inspection")
    print("=" * 80)
    
    # Load vector store
    print("\nLoading vector store...")
    vector_store = VectorStore.load(args.vector_store_dir)
    
    total_chunks = len(vector_store.chunks)
    print(f"Total chunks in store: {total_chunks}")
    
    # Sample random chunks
    sample_size = min(args.sample, total_chunks)
    sampled_chunks = random.sample(vector_store.chunks, sample_size)
    
    print(f"\nDisplaying {sample_size} random chunks:")
    print("=" * 80)
    
    for i, chunk in enumerate(sampled_chunks, 1):
        print(f"\n{'='*80}")
        print(f"CHUNK {i}/{sample_size}")
        print(f"{'='*80}")
        print(f"Source: {chunk.metadata.get('relative_path', 'unknown')}")
        print(f"Section: {chunk.metadata.get('section_title', 'N/A')}")
        print(f"Chunk Index: {chunk.metadata.get('chunk_index', 'N/A')}")
        print(f"Token Count: {chunk.metadata.get('token_count', 'N/A')}")
        print(f"\nContent:")
        print("-" * 80)
        print(chunk.text)
        print("-" * 80)


if __name__ == "__main__":
    main()
