"""Utility functions for text processing and chunking."""

import re
import tiktoken
from typing import List, Tuple


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count the number of tokens in text using tiktoken.
    
    Args:
        text: Text to count tokens for
        encoding_name: Encoding to use (default: cl100k_base for GPT-4)
        
    Returns:
        Number of tokens in text
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def clean_text(text: str) -> str:
    """Clean text by normalizing whitespace and formatting.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def detect_section_header(line: str) -> Tuple[bool, int]:
    """Detect if a line is a section header and determine its level.
    
    Python docs use underlines with special characters to mark sections:
    - '***' for main titles
    - '===' for level 1 headers
    - '---' for level 2 headers
    
    Args:
        line: Line to check
        
    Returns:
        Tuple of (is_header, level) where level is 0 if not a header
    """
    stripped = line.strip()
    
    # Check for underline-style headers
    if len(stripped) >= 3:
        if all(c == '*' for c in stripped):
            return True, 1
        elif all(c == '=' for c in stripped):
            return True, 2
        elif all(c == '-' for c in stripped):
            return True, 3
    
    return False, 0


def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences (simple heuristic).
    
    Args:
        text: Text to split
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting on periods, question marks, exclamation marks
    # followed by whitespace or end of string
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def extract_section_title(lines: List[str], header_index: int) -> str:
    """Extract section title from lines given header underline index.
    
    Args:
        lines: List of text lines
        header_index: Index of the header underline
        
    Returns:
        Section title (line above the underline)
    """
    if header_index > 0:
        return lines[header_index - 1].strip()
    return ""
