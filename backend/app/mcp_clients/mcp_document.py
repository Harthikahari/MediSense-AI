"""
MCP Document client for document search, retrieval, and OCR operations.
"""

from typing import Any, Dict, List, Optional
from .mcp_base import ToolClient, get_mcp_client
from app.core.logger import get_logger

logger = get_logger(__name__)


class DocumentMCPClient:
    """
    MCP client for document operations including:
    - Document search and retrieval
    - OCR processing
    - Text extraction from PDFs
    """

    def __init__(self, client: Optional[ToolClient] = None):
        """
        Initialize document MCP client.

        Args:
            client: Optional MCP client instance (defaults to configured client)
        """
        self.client = client or get_mcp_client()

    async def search_documents(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search documents by query string.

        Args:
            query: Search query
            filters: Optional filters (e.g., document type, date range)
            top_k: Number of results to return

        Returns:
            List of matching documents with metadata
        """
        payload = {
            "query": query,
            "filters": filters or {},
            "top_k": top_k
        }

        logger.info("Searching documents", query=query, top_k=top_k)
        result = await self.client.call_tool("search_documents", payload)
        return result.get("results", [])

    async def fetch_document(self, document_id: str) -> Dict[str, Any]:
        """
        Fetch a specific document by ID.

        Args:
            document_id: Document identifier

        Returns:
            Document data and metadata
        """
        payload = {"document_id": document_id}

        logger.info("Fetching document", document_id=document_id)
        result = await self.client.call_tool("fetch_document", payload)
        return result

    async def ocr_document(
        self,
        image_path: str,
        language: str = "eng"
    ) -> Dict[str, Any]:
        """
        Perform OCR on a document image.

        Args:
            image_path: Path to image file
            language: OCR language (default: English)

        Returns:
            Extracted text and metadata
        """
        payload = {
            "image_path": image_path,
            "language": language
        }

        logger.info("Performing OCR", image_path=image_path)
        result = await self.client.call_tool("ocr_document", payload)
        return result

    async def extract_pdf_text(
        self,
        pdf_path: str,
        page_range: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """
        Extract text from PDF document.

        Args:
            pdf_path: Path to PDF file
            page_range: Optional tuple of (start_page, end_page)

        Returns:
            Extracted text and page metadata
        """
        payload = {
            "pdf_path": pdf_path,
            "page_range": page_range
        }

        logger.info("Extracting PDF text", pdf_path=pdf_path)
        result = await self.client.call_tool("extract_pdf_text", payload)
        return result

    async def extract_structured_data(
        self,
        document_content: str,
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract structured data from document using LLM-assisted extraction.

        Args:
            document_content: Document text content
            schema: Expected data schema

        Returns:
            Extracted structured data
        """
        payload = {
            "content": document_content,
            "schema": schema
        }

        logger.info("Extracting structured data", schema_keys=list(schema.keys()))
        result = await self.client.call_tool("extract_structured_data", payload)
        return result

    async def chunk_document(
        self,
        document_content: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Split document into chunks for RAG indexing.

        Args:
            document_content: Document text
            chunk_size: Size of each chunk (in tokens/characters)
            overlap: Overlap between chunks

        Returns:
            List of document chunks with metadata
        """
        payload = {
            "content": document_content,
            "chunk_size": chunk_size,
            "overlap": overlap
        }

        logger.info("Chunking document", chunk_size=chunk_size, overlap=overlap)
        result = await self.client.call_tool("chunk_document", payload)
        return result.get("chunks", [])
