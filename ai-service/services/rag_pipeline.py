"""
RAG (Retrieval Augmented Generation) Pipeline for incident response documentation.
Loads documents, chunks them, embeds with sentence-transformers, stores in ChromaDB.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Manages document loading, chunking, embedding, and retrieval from ChromaDB."""
    
    def __init__(
        self,
        collection_name: str = "incident_response_docs",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "all-MiniLM-L6-v2",
        chroma_db_dir: str = None
    ):
        """Initialize RAG pipeline.
        
        Args:
            collection_name: Name of ChromaDB collection
            chunk_size: Size of text chunks in characters (default: 500)
            chunk_overlap: Overlap between chunks in characters (default: 50)
            embedding_model: Sentence transformer model to use
            chroma_db_dir: Directory to store ChromaDB (default: ./chroma_data)
        """
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model
        
        # Set up ChromaDB directory
        if chroma_db_dir is None:
            chroma_db_dir = os.path.join(os.path.dirname(__file__), "..", "chroma_data")
        
        os.makedirs(chroma_db_dir, exist_ok=True)
        self.chroma_db_dir = chroma_db_dir
        
        logger.info(f"Initializing RAG pipeline with model: {embedding_model}")
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer(embedding_model)
            logger.info(f"Loaded embedding model: {embedding_model}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {str(e)}")
            raise
        
        # Initialize ChromaDB client
        try:
            self.client = chromadb.PersistentClient(path=chroma_db_dir)
            logger.info(f"Initialized ChromaDB at {chroma_db_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            raise
        
        # Get or create collection
        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Got/created collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to get/create collection: {str(e)}")
            raise
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        chunks = []
        text_length = len(text)
        
        if text_length <= self.chunk_size:
            return [text]
        
        start = 0
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move start position, accounting for overlap
            start = end - self.chunk_overlap
            
            # Prevent infinite loops on very small overlaps
            if start >= end - self.chunk_overlap:
                start = end
        
        logger.debug(f"Split text of {text_length} chars into {len(chunks)} chunks")
        return chunks
    
    def load_documents_from_directory(self, docs_dir: str) -> List[Dict[str, Any]]:
        """Load all text documents from a directory.
        
        Args:
            docs_dir: Directory containing .txt files
            
        Returns:
            List of document dictionaries with content and metadata
        """
        documents = []
        docs_path = Path(docs_dir)
        
        if not docs_path.exists():
            logger.error(f"Documents directory not found: {docs_dir}")
            return documents
        
        # Load all .txt files
        txt_files = list(docs_path.glob("*.txt"))
        logger.info(f"Found {len(txt_files)} text files in {docs_dir}")
        
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                documents.append({
                    "filename": file_path.name,
                    "content": content,
                    "path": str(file_path)
                })
                logger.info(f"Loaded document: {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {str(e)}")
        
        return documents
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        """Add documents to the RAG pipeline.
        
        Chunks each document, embeds chunks, and stores in ChromaDB.
        
        Args:
            documents: List of document dictionaries with 'content' and 'filename'
            
        Returns:
            Total number of chunks stored
        """
        total_chunks = 0
        
        for doc in documents:
            try:
                filename = doc.get("filename", "unknown")
                content = doc.get("content", "")
                
                # Chunk the document
                chunks = self.chunk_text(content)
                
                # Generate embeddings for each chunk
                embeddings = self.embedding_model.encode(chunks).tolist()
                
                # Prepare data for ChromaDB
                ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
                metadatas = [
                    {
                        "filename": filename,
                        "chunk_index": i,
                        "char_count": len(chunk)
                    }
                    for i, chunk in enumerate(chunks)
                ]
                
                # Add to collection
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=chunks
                )
                
                total_chunks += len(chunks)
                logger.info(f"Added {len(chunks)} chunks from {filename}")
            
            except Exception as e:
                logger.error(f"Failed to add document {doc.get('filename')}: {str(e)}")
        
        logger.info(f"Added total of {total_chunks} chunks to collection")
        return total_chunks
    
    def query(self, query_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Query the RAG pipeline for relevant documents.
        
        Args:
            query_text: Query text
            n_results: Number of results to return
            
        Returns:
            List of relevant document chunks with metadata
        """
        try:
            # Query ChromaDB (new API doesn't require manual embedding)
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results and results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else None
                    })
            
            logger.info(f"Query returned {len(formatted_results)} results")
            return formatted_results
        
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the current collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_model": self.embedding_model_name,
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
                "chroma_db_dir": self.chroma_db_dir
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            return {}
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Cleared collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear collection: {str(e)}")
            return False
