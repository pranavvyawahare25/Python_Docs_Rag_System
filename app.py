"""Streamlit web interface for Python Docs RAG System."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.embedder import Embedder
from src.vector_store import VectorStore


# Page configuration
st.set_page_config(
    page_title="Python Docs RAG Assistant",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #3776ab;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3776ab;
        margin-bottom: 1rem;
    }
    .metadata {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .similarity-score {
        display: inline-block;
        background-color: #3776ab;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 0.3rem;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_rag_system():
    """Load the vector store and embedder (cached)."""
    try:
        vector_store = VectorStore.load("data/vector_store")
        embedder = Embedder(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return vector_store, embedder
    except Exception as e:
        st.error(f"Error loading RAG system: {str(e)}")
        st.info("Make sure you've run the ingestion pipeline first:\n```bash\npython3.8 -m src.ingest --docs-path /path/to/python-docs\n```")
        return None, None


def format_similarity_score(distance):
    """Convert L2 distance to similarity percentage."""
    similarity = 1 / (1 + distance)
    return similarity * 100


def main():
    # Header
    st.markdown('<p class="main-header">🐍 Python Documentation Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask questions about Python and get answers from official documentation</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Info")
        
        # Load system
        vector_store, embedder = load_rag_system()
        
        if vector_store and embedder:
            st.success("✅ RAG System Loaded")
            st.metric("Total Chunks", len(vector_store.chunks))
            st.metric("Embedding Dimension", embedder.embedding_dim)
            
            st.divider()
            
            st.header("⚙️ Settings")
            top_k = st.slider("Number of results", min_value=1, max_value=10, value=3)
            show_metadata = st.checkbox("Show detailed metadata", value=True)
            show_full_text = st.checkbox("Show full chunk text", value=False)
            
            st.divider()
            
            st.header("💡 Example Questions")
            st.markdown("""
            - What are Python's built-in data types?
            - How do I use list comprehensions?
            - Explain string slicing in Python
            - How do decorators work?
            - What is exception handling?
            - How to read and write files?
            """)
        else:
            st.error("❌ RAG System Not Loaded")
            return
    
    # Main content
    if vector_store and embedder:
        # Query input
        query = st.text_input(
            "Ask your question:",
            placeholder="e.g., How do I use list comprehensions in Python?",
            key="query_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        with col2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.rerun()
        
        # Process query
        if search_button and query:
            with st.spinner("Searching documentation..."):
                # Generate query embedding
                query_embedding = embedder.embed_query(query)
                
                # Search vector store
                results = vector_store.search(query_embedding, k=top_k)
                
                # Display results
                st.divider()
                st.subheader(f"📚 Top {len(results)} Results")
                
                for i, (chunk, distance) in enumerate(results, 1):
                    similarity_pct = format_similarity_score(distance)
                    
                    with st.container():
                        st.markdown(f"### Result {i}")
                        
                        # Similarity score badge
                        st.markdown(
                            f'<span class="similarity-score">Similarity: {similarity_pct:.1f}%</span>',
                            unsafe_allow_html=True
                        )
                        
                        # Metadata
                        if show_metadata:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.markdown(f"**📄 Source:** `{chunk.metadata.get('filename', 'N/A')}`")
                            with col2:
                                st.markdown(f"**📑 Section:** {chunk.metadata.get('section_title', 'N/A')}")
                            with col3:
                                st.markdown(f"**🔢 Tokens:** {chunk.metadata.get('token_count', 'N/A')}")
                        
                        # Content
                        st.markdown("**Content:**")
                        if show_full_text:
                            st.markdown(f"```\n{chunk.text}\n```")
                        else:
                            preview = chunk.text[:500] + "..." if len(chunk.text) > 500 else chunk.text
                            st.markdown(f"```\n{preview}\n```")
                            if len(chunk.text) > 500:
                                with st.expander("Show full text"):
                                    st.markdown(f"```\n{chunk.text}\n```")
                        
                        st.divider()
                
                # Summary
                st.info(f"💡 Found {len(results)} relevant sections from Python documentation. The similarity scores indicate how well each result matches your query.")
        
        elif query and not search_button:
            st.info("👆 Click the Search button to find relevant documentation")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Built with Streamlit • Python Documentation RAG System</p>
        <p>Powered by sentence-transformers & FAISS</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
