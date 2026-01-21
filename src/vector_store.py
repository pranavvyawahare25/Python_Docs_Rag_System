"""FAISS-based vector store for efficient similarity search."""

import json
import numpy as np
import faiss
from pathlib import Path
from typing import List, Tuple, Dict
from src.chunker import Chunk


class VectorStore:
    """FAISS vector store for document chunks."""
    
    def __init__(self, embedding_dim: int):
        """Initialize vector store.
        
        Args:
            embedding_dim: Dimension of embeddings
        """
        self.embedding_dim = embedding_dim
        # Use IndexFlatL2 for exact search (good for learning/small datasets)
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks = []  # Store chunk objects
        
    def add_chunks(self, chunks: List[Chunk], embeddings: np.ndarray):
        """Add chunks and their embeddings to the index.
        
        Args:
            chunks: List of Chunk objects
            embeddings: Numpy array of embeddings (num_chunks, embedding_dim)
        """
        if embeddings.shape[0] != len(chunks):
            raise ValueError("Number of embeddings must match number of chunks")
        
        # Ensure embeddings are float32 (required by FAISS)
        embeddings = embeddings.astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store chunks
        self.chunks.extend(chunks)
        
        print(f"Added {len(chunks)} chunks to vector store. Total: {self.index.ntotal}")
        
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Chunk, float]]:
        """Search for most similar chunks.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of (Chunk, distance) tuples, sorted by similarity
        """
        # Ensure query is 2D array
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        query_embedding = query_embedding.astype('float32')
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Prepare results
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx != -1:  # -1 means not found
                results.append((self.chunks[idx], float(dist)))
        
        return results
    
    def save(self, save_dir: str):
        """Save index and chunks to disk.
        
        Args:
            save_dir: Directory to save files
        """
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = save_path / "faiss_index.bin"
        faiss.write_index(self.index, str(index_path))
        print(f"Saved FAISS index to {index_path}")
        
        # Save chunk metadata
        chunks_data = []
        for chunk in self.chunks:
            chunks_data.append({
                'text': chunk.text,
                'metadata': chunk.metadata
            })
        
        metadata_path = save_path / "chunks_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(chunks_data, f, indent=2, ensure_ascii=False)
        print(f"Saved chunk metadata to {metadata_path}")
        
    @classmethod
    def load(cls, load_dir: str) -> 'VectorStore':
        """Load index and chunks from disk.
        
        Args:
            load_dir: Directory containing saved files
            
        Returns:
            VectorStore instance
        """
        load_path = Path(load_dir)
        
        # Load FAISS index
        index_path = load_path / "faiss_index.bin"
        if not index_path.exists():
            raise FileNotFoundError(f"Index file not found: {index_path}")
        
        index = faiss.read_index(str(index_path))
        
        # Load chunk metadata
        metadata_path = load_path / "chunks_metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            chunks_data = json.load(f)
        
        # Reconstruct chunks
        chunks = []
        for chunk_data in chunks_data:
            chunk = Chunk(
                text=chunk_data['text'],
                metadata=chunk_data['metadata']
            )
            chunks.append(chunk)
        
        # Create vector store instance
        embedding_dim = index.d
        vector_store = cls(embedding_dim)
        vector_store.index = index
        vector_store.chunks = chunks
        
        print(f"Loaded vector store with {index.ntotal} chunks from {load_dir}")
        
        return vector_store
