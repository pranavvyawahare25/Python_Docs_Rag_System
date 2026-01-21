"""Document loader for Python documentation files."""

import os
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Document:
    """Represents a loaded document with metadata."""
    content: str
    metadata: Dict[str, str]
    
    def __repr__(self):
        return f"Document(source={self.metadata.get('source', 'unknown')}, length={len(self.content)})"


class DocLoader:
    """Loads Python documentation text files."""
    
    def __init__(self, docs_base_path: str):
        """Initialize document loader.
        
        Args:
            docs_base_path: Base path to Python docs directory
        """
        self.docs_base_path = Path(docs_base_path)
        
    def load_tutorial_files(self) -> List[Document]:
        """Load all .txt files from the tutorial directory.
        
        Returns:
            List of Document objects
        """
        tutorial_path = self.docs_base_path / "tutorial"
        
        if not tutorial_path.exists():
            raise FileNotFoundError(f"Tutorial directory not found: {tutorial_path}")
        
        documents = []
        for txt_file in sorted(tutorial_path.glob("*.txt")):
            doc = self._load_file(txt_file, doc_type="tutorial")
            documents.append(doc)
            
        return documents
    
    def load_library_files(self, filenames: List[str]) -> List[Document]:
        """Load specific library documentation files.
        
        Args:
            filenames: List of filenames in library/ directory (e.g., ['stdtypes.txt'])
            
        Returns:
            List of Document objects
        """
        library_path = self.docs_base_path / "library"
        
        if not library_path.exists():
            raise FileNotFoundError(f"Library directory not found: {library_path}")
        
        documents = []
        for filename in filenames:
            file_path = library_path / filename
            if not file_path.exists():
                print(f"Warning: File not found: {file_path}")
                continue
                
            doc = self._load_file(file_path, doc_type="library")
            documents.append(doc)
            
        return documents
    
    def load_all_specified(self) -> List[Document]:
        """Load all documents in the specified scope.
        
        Returns:
            List of all Document objects
        """
        documents = []
        
        # Load tutorial files
        print("Loading tutorial files...")
        tutorial_docs = self.load_tutorial_files()
        documents.extend(tutorial_docs)
        print(f"  Loaded {len(tutorial_docs)} tutorial files")
        
        # Load specified library files
        print("Loading library files...")
        library_files = ["stdtypes.txt", "functions.txt"]
        library_docs = self.load_library_files(library_files)
        documents.extend(library_docs)
        print(f"  Loaded {len(library_docs)} library files")
        
        return documents
    
    def _load_file(self, file_path: Path, doc_type: str) -> Document:
        """Load a single text file.
        
        Args:
            file_path: Path to the file
            doc_type: Type of document (tutorial, library, etc.)
            
        Returns:
            Document object
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            metadata = {
                'source': str(file_path),
                'filename': file_path.name,
                'doc_type': doc_type,
                'relative_path': str(file_path.relative_to(self.docs_base_path))
            }
            
            return Document(content=content, metadata=metadata)
            
        except UnicodeDecodeError:
            print(f"Warning: Could not decode {file_path} as UTF-8, trying latin-1")
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
                
            metadata = {
                'source': str(file_path),
                'filename': file_path.name,
                'doc_type': doc_type,
                'relative_path': str(file_path.relative_to(self.docs_base_path))
            }
            
            return Document(content=content, metadata=metadata)
