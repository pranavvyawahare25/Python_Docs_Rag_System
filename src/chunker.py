"""Text chunker with semantic awareness for Python documentation."""

from typing import List, Dict
from dataclasses import dataclass
from src.doc_loader import Document
from src.utils import count_tokens, detect_section_header, extract_section_title


@dataclass
class Chunk:
    """Represents a text chunk with metadata."""
    text: str
    metadata: Dict[str, str]
    
    def __repr__(self):
        return f"Chunk(source={self.metadata.get('source', 'unknown')}, tokens={self.metadata.get('token_count', 0)})"


class SemanticChunker:
    """Chunks documents based on semantic structure (sections)."""
    
    def __init__(
        self,
        target_chunk_size: int = 512,
        max_chunk_size: int = 1024,
        overlap_size: int = 128
    ):
        """Initialize chunker.
        
        Args:
            target_chunk_size: Target number of tokens per chunk
            max_chunk_size: Maximum number of tokens per chunk
            overlap_size: Number of tokens to overlap between chunks
        """
        self.target_chunk_size = target_chunk_size
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
        
    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        """Chunk a list of documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of Chunk objects
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
            
        return all_chunks
    
    def chunk_document(self, document: Document) -> List[Chunk]:
        """Chunk a single document based on sections.
        
        Args:
            document: Document to chunk
            
        Returns:
            List of Chunk objects
        """
        lines = document.content.split('\n')
        sections = self._split_into_sections(lines)
        
        chunks = []
        for section_title, section_content in sections:
            # Chunk each section
            section_chunks = self._chunk_section(
                section_content,
                section_title,
                document.metadata
            )
            chunks.extend(section_chunks)
            
        return chunks
    
    def _split_into_sections(self, lines: List[str]) -> List[tuple]:
        """Split document into sections based on headers.
        
        Args:
            lines: List of document lines
            
        Returns:
            List of (section_title, section_content) tuples
        """
        sections = []
        current_section_title = "Introduction"
        current_section_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            is_header, level = detect_section_header(line)
            
            if is_header and i > 0:
                # Found a section header, save previous section
                if current_section_lines:
                    sections.append((
                        current_section_title,
                        '\n'.join(current_section_lines).strip()
                    ))
                
                # Start new section
                current_section_title = extract_section_title(lines, i)
                current_section_lines = []
                i += 1  # Skip the header line
            else:
                current_section_lines.append(line)
                i += 1
        
        # Add the last section
        if current_section_lines:
            sections.append((
                current_section_title,
                '\n'.join(current_section_lines).strip()
            ))
        
        return sections
    
    def _chunk_section(
        self,
        section_content: str,
        section_title: str,
        doc_metadata: Dict[str, str]
    ) -> List[Chunk]:
        """Chunk a single section into appropriately sized chunks.
        
        Args:
            section_content: Section text content
            section_title: Title of the section
            doc_metadata: Metadata from parent document
            
        Returns:
            List of Chunk objects
        """
        token_count = count_tokens(section_content)
        
        # If section fits in target size, return as single chunk
        if token_count <= self.target_chunk_size:
            metadata = {
                **doc_metadata,
                'section_title': section_title,
                'token_count': str(token_count),
                'chunk_index': '0'
            }
            return [Chunk(text=section_content, metadata=metadata)]
        
        # Otherwise, split into smaller chunks with overlap
        chunks = []
        paragraphs = [p.strip() for p in section_content.split('\n\n') if p.strip()]
        
        current_chunk_text = ""
        current_chunk_tokens = 0
        chunk_index = 0
        
        for para in paragraphs:
            para_tokens = count_tokens(para)
            
            # If adding this paragraph exceeds max size, save current chunk
            if current_chunk_tokens + para_tokens > self.max_chunk_size and current_chunk_text:
                metadata = {
                    **doc_metadata,
                    'section_title': section_title,
                    'token_count': str(current_chunk_tokens),
                    'chunk_index': str(chunk_index)
                }
                chunks.append(Chunk(text=current_chunk_text.strip(), metadata=metadata))
                
                # Start new chunk with overlap (last sentences of previous chunk)
                overlap_text = self._get_overlap_text(current_chunk_text, self.overlap_size)
                current_chunk_text = overlap_text + "\n\n" + para
                current_chunk_tokens = count_tokens(current_chunk_text)
                chunk_index += 1
            else:
                # Add paragraph to current chunk
                if current_chunk_text:
                    current_chunk_text += "\n\n" + para
                else:
                    current_chunk_text = para
                current_chunk_tokens += para_tokens
        
        # Add final chunk
        if current_chunk_text:
            metadata = {
                **doc_metadata,
                'section_title': section_title,
                'token_count': str(current_chunk_tokens),
                'chunk_index': str(chunk_index)
            }
            chunks.append(Chunk(text=current_chunk_text.strip(), metadata=metadata))
        
        return chunks
    
    def _get_overlap_text(self, text: str, overlap_tokens: int) -> str:
        """Get the last N tokens worth of text for overlap.
        
        Args:
            text: Full text
            overlap_tokens: Number of tokens to include in overlap
            
        Returns:
            Overlap text
        """
        # Simple heuristic: take last few sentences
        sentences = text.split('. ')
        if len(sentences) <= 2:
            return ""
        
        # Take last 2 sentences as overlap
        return '. '.join(sentences[-2:])
