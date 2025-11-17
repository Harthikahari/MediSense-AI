"""
RAG (Retrieval-Augmented Generation) Agent for document retrieval and context assembly.
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentTask, AgentResult
from app.mcp_clients import DocumentMCPClient


class RAGAgent(BaseAgent):
    """
    RAG agent for retrieving relevant documents and assembling context.
    Uses vector database for semantic search.
    """

    def __init__(self, document_client: Optional[DocumentMCPClient] = None):
        """Initialize RAG agent."""
        super().__init__("rag_agent")
        self.document_client = document_client or DocumentMCPClient()
        self.max_context_tokens = 4000  # Maximum context size

    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute RAG retrieval and response generation.

        Args:
            task: Agent task with query

        Returns:
            RAG response with sources and provenance
        """
        try:
            query = task.query
            top_k = task.context.get("top_k", 5)

            # Retrieve relevant documents
            self.logger.info("Retrieving documents", query=query, top_k=top_k)
            documents = await self.document_client.search_documents(
                query=query,
                filters=task.context.get("filters"),
                top_k=top_k
            )

            if not documents:
                return self.create_success_result(
                    task_id=task.task_id,
                    response={
                        "answer": "No relevant documents found for your query.",
                        "sources": [],
                        "confidence": 0.0
                    },
                    confidence=0.0
                )

            # Assemble context from retrieved documents
            context = self._assemble_context(documents)

            # Generate response (simplified - in production, call LLM via MCP)
            answer = self._generate_answer(query, context, documents)

            # Build provenance
            provenance = [
                {
                    "source_id": doc.get("id"),
                    "title": doc.get("title"),
                    "score": doc.get("score")
                }
                for doc in documents
            ]

            return self.create_success_result(
                task_id=task.task_id,
                response={
                    "answer": answer,
                    "sources": documents,
                    "confidence": self._calculate_confidence(documents)
                },
                confidence=self._calculate_confidence(documents),
                provenance=provenance
            )

        except Exception as e:
            self.logger.error(f"RAG execution failed: {str(e)}")
            return self.create_error_result(
                task_id=task.task_id,
                error=f"RAG agent failed: {str(e)}"
            )

    def _assemble_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Assemble context from retrieved documents.

        Args:
            documents: List of retrieved documents

        Returns:
            Assembled context string
        """
        context_parts = []
        total_length = 0
        max_length = self.max_context_tokens * 4  # Approximate characters

        for doc in documents:
            content = doc.get("content", "")
            if total_length + len(content) > max_length:
                # Truncate if exceeds max length
                remaining = max_length - total_length
                content = content[:remaining] + "..."

            context_parts.append(f"[{doc.get('title', 'Untitled')}]\n{content}\n")
            total_length += len(content)

            if total_length >= max_length:
                break

        return "\n---\n".join(context_parts)

    def _generate_answer(
        self,
        query: str,
        context: str,
        documents: List[Dict[str, Any]]
    ) -> str:
        """
        Generate answer from context (simplified implementation).

        In production, this would call an LLM via MCP with the context.

        Args:
            query: User query
            context: Assembled context
            documents: Retrieved documents

        Returns:
            Generated answer
        """
        # Simplified answer generation
        # In production: call LLM with prompt template
        if not documents:
            return "I couldn't find relevant information to answer your question."

        return (
            f"Based on {len(documents)} relevant documents, I found information related to your query. "
            f"The most relevant document is '{documents[0].get('title', 'Untitled')}' "
            f"with a relevance score of {documents[0].get('score', 0):.2f}. "
            f"[In production, this would be a comprehensive LLM-generated answer using the retrieved context.]"
        )

    def _calculate_confidence(self, documents: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score based on retrieval results.

        Args:
            documents: Retrieved documents

        Returns:
            Confidence score (0-1)
        """
        if not documents:
            return 0.0

        # Use average of top 3 document scores
        top_scores = [doc.get("score", 0) for doc in documents[:3]]
        return sum(top_scores) / len(top_scores) if top_scores else 0.5
