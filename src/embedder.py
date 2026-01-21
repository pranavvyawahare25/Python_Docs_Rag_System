"""Embedding generator using sentence-transformers."""

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from src.chunker import Chunk


class Embedder:
    """Generates embeddings for text chunks using sentence-transformers."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize embedder.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"  Model loaded. Embedding dimension: {self.embedding_dim}")
        
    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for a list of chunks.
        
        Args:
            chunks: List of Chunk objects
            batch_size: Batch size for encoding
            
        Returns:
            Numpy array of shape (num_chunks, embedding_dim)
        """
        texts = [chunk.text for chunk in chunks]
        
        print(f"Generating embeddings for {len(texts)} chunks...")
        
        # Encode in batches with progress bar
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True  # L2 normalization for cosine similarity
        )
        
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for a single query.
        
        Args:
            query: Query text
            
        Returns:
            Numpy array of shape (embedding_dim,)
        """
        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )
        return embedding
