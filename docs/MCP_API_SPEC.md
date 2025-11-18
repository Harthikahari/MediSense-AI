# MCP API Specification

## Model Context Protocol (MCP) for MediSense-AI

The MCP layer provides a unified interface for external service integration with support for both mock (development) and production (Anthropic) modes.

## Base Client Interface

All MCP clients implement the `ToolClient` interface:

```python
class ToolClient(ABC):
    async def call_tool(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool with given name and payload."""
        pass
```

## MCP Clients

### 1. Document MCP Client

**Purpose**: Document operations including search, retrieval, OCR, and text extraction.

#### Operations

##### search_documents
```python
payload = {
    "query": str,           # Search query
    "filters": dict,        # Optional filters
    "top_k": int           # Number of results (default: 5)
}

response = {
    "results": [
        {
            "id": str,
            "title": str,
            "content": str,
            "score": float
        }
    ]
}
```

##### ocr_document
```python
payload = {
    "image_path": str,      # Path to image file
    "language": str         # OCR language (default: "eng")
}

response = {
    "text": str,
    "confidence": float,
    "metadata": dict
}
```

##### extract_pdf_text
```python
payload = {
    "pdf_path": str,
    "page_range": tuple    # Optional (start_page, end_page)
}

response = {
    "text": str,
    "pages": int,
    "metadata": dict
}
```

### 2. Database MCP Client

**Purpose**: Safe, parameterized SQL query execution with read-only access.

#### Operations

##### execute_query
```python
payload = {
    "query": str,          # SQL query with placeholders
    "params": dict,        # Query parameters
    "read_only": bool      # Enforce read-only (default: True)
}

response = {
    "rows": list,
    "row_count": int,
    "columns": list
}
```

##### get_appointment_slots
```python
payload = {
    "clinician_id": int,
    "date": str,           # YYYY-MM-DD format
    "duration_minutes": int
}

response = {
    "slots": [
        {
            "start_time": str,
            "end_time": str,
            "available": bool
        }
    ]
}
```

### 3. Model MCP Client

**Purpose**: ONNX model inference for image classification and segmentation.

#### Operations

##### classify_image
```python
payload = {
    "image_data": str,     # Base64-encoded image
    "model_name": str,
    "top_k": int
}

response = {
    "predictions": [
        {
            "label": str,
            "confidence": float
        }
    ]
}
```

##### segment_image
```python
payload = {
    "image_data": str,
    "model_name": str
}

response = {
    "mask": str,           # Base64-encoded segmentation mask
    "bounding_boxes": list,
    "area_pixels": int,
    "confidence": float
}
```

### 4. Payment MCP Client

**Purpose**: Payment gateway integration (sandbox mode).

#### Operations

##### create_payment_intent
```python
payload = {
    "amount": float,
    "currency": str,       # Default: "USD"
    "customer_id": str,
    "metadata": dict
}

response = {
    "payment_intent_id": str,
    "client_secret": str,
    "status": str
}
```

##### process_payment
```python
payload = {
    "payment_intent_id": str,
    "payment_method": str,
    "billing_details": dict
}

response = {
    "transaction_id": str,
    "status": str,
    "amount": float
}
```

### 5. Notification MCP Client

**Purpose**: Email and SMS notification delivery.

#### Operations

##### send_email
```python
payload = {
    "to_email": str,
    "subject": str,
    "body": str,
    "template_name": str,   # Optional
    "template_vars": dict,
    "attachments": list
}

response = {
    "message_id": str,
    "status": str
}
```

##### send_sms
```python
payload = {
    "to_phone": str,
    "message": str,
    "template_name": str,   # Optional
    "template_vars": dict
}

response = {
    "message_id": str,
    "status": str
}
```

## MCP Modes

### Mock Mode (Development)

Activated with `MCP_MODE=mock` in environment.

- Returns simulated responses
- No external API calls
- Useful for testing and development
- Predictable response times

### Anthropic Mode (Production)

Activated with `MCP_MODE=anthropic` and valid `ANTHROPIC_API_KEY`.

- Connects to Anthropic API
- Real LLM inference
- Requires API key authentication
- Implements retry logic and error handling

## Error Handling

All MCP operations follow consistent error handling:

```python
try:
    result = await mcp_client.call_tool(name, payload)
except Exception as e:
    # Returns error response
    {
        "error": str(e),
        "status": "failed"
    }
```

## Authentication

MCP clients use one of:
- API key authentication (Authorization header)
- mTLS for secure server communication
- Environment-based configuration

## Rate Limiting

- Configurable per-client
- Default: 60 requests/minute
- Timeout: 30 seconds (configurable)

## Monitoring

All MCP calls are logged with:
- Request timestamp
- Tool name
- Payload (redacted)
- Response status
- Execution time

## Best Practices

1. **Always use parameterized queries** in Database MCP
2. **Validate input** before calling MCP tools
3. **Handle timeouts** gracefully
4. **Log all operations** for audit trail
5. **Use mock mode** for testing
6. **Implement retries** for transient failures

## Example Usage

```python
from app.mcp_clients import DocumentMCPClient

# Initialize client
doc_client = DocumentMCPClient()

# Search documents
results = await doc_client.search_documents(
    query="patient medical history",
    filters={"date_from": "2024-01-01"},
    top_k=10
)

print(f"Found {len(results)} documents")
```

---

**Version**: 1.0.0
**Last Updated**: 2025-01-17
