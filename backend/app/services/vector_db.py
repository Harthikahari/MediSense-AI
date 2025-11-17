"""
Vector database service using Chroma.
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from app.core.config import settings
from app.core.logger import get_logger
from app.services.embedding_service import get_embedding_service

logger = get_logger(__name__)


class VectorDBService:
    """Service for vector database operations using Chroma."""

    def __init__(self):
        """Initialize vector database service."""
        logger.info("Initializing Chroma vector database")

        # Initialize Chroma client
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.CHROMA_PERSIST_DIR
        ))

        # Initialize embedding service
        self.embedding_service = get_embedding_service()

        logger.info("Chroma vector database initialized")

    def get_or_create_collection(self, collection_name: str) -> Any:
        """
        Get or create a collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object
        """
        return self.client.get_or_create_collection(name=collection_name)

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ):
        """
        Add documents to a collection.

        Args:
            collection_name: Name of the collection
            documents: List of document texts
            metadatas: Optional list of metadata dicts
            ids: Optional list of document IDs
        """
        collection = self.get_or_create_collection(collection_name)

        # Generate embeddings
        embeddings = self.embedding_service.encode(documents)

        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        # Add to collection
        collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        logger.info(f"Added {len(documents)} documents to collection {collection_name}")

    def search(
        self,
        collection_name: str,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for similar documents.

        Args:
            collection_name: Name of the collection
            query: Query text
            n_results: Number of results to return
            where: Optional filter conditions

        Returns:
            Search results
        """
        collection = self.get_or_create_collection(collection_name)

        # Generate query embedding
        query_embedding = self.embedding_service.encode_single(query)

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )

        # Format results
        formatted_results = []
        if results["documents"] and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                })

        return {
            "results": formatted_results,
            "count": len(formatted_results)
        }

    def delete_collection(self, collection_name: str):
        """Delete a collection."""
        self.client.delete_collection(name=collection_name)
        logger.info(f"Deleted collection {collection_name}")


# Global vector DB service instance
_vector_db_service = None


def get_vector_db_service() -> VectorDBService:
    """Get global vector DB service instance."""
    global _vector_db_service
    if _vector_db_service is None:
        _vector_db_service = VectorDBService()
    return _vector_db_service
