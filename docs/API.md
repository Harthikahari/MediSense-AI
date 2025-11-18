# API Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.medisense-ai.com
```

## Authentication

All API requests (except `/auth/register` and `/auth/login`) require authentication using JWT tokens.

### Headers

```http
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## Endpoints

### Authentication

#### Register User

```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "role": "patient",
  "phone_number": "+1234567890"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "patient",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-01-17T12:00:00Z"
}
```

#### Login

```http
POST /api/v1/auth/login?email=user@example.com&password=securepassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Agent Endpoints

#### Chat with Auto-Routing

```http
POST /api/v1/agents/chat
```

**Request Body:**
```json
{
  "query": "I need to book an appointment with a cardiologist",
  "context": {},
  "session_id": null
}
```

**Response:**
```json
{
  "agent_name": "appointment",
  "response": "I can help you book an appointment...",
  "confidence": 0.95,
  "provenance": [...],
  "metadata": {
    "routing_confidence": 0.98,
    "guardrails_applied": 0
  }
}
```

#### Call Specific Agent

```http
POST /api/v1/agents/agent/{agent_name}
```

**Available Agents:**
- `routing` - Intent classification
- `rag` - Document retrieval
- `sql` - Database queries
- `appointment` - Appointment booking
- `payment` - Payment processing
- `image` - Image analysis
- `report` - Report processing
- `prescription` - Prescription generation
- `guardrail` - Safety checking
- `audit` - Audit operations

#### List Available Agents

```http
GET /api/v1/agents/agents
```

**Response:**
```json
{
  "agents": ["routing", "rag", "sql", "appointment", ...],
  "count": 11
}
```

### MCP Endpoints

#### Search Documents

```http
POST /api/v1/mcp/document/search
```

**Request Body:**
```json
{
  "query": "patient medical history",
  "top_k": 5,
  "filters": {}
}
```

#### Classify Image

```http
POST /api/v1/mcp/model/classify
```

**Request Body:**
```json
{
  "image_data": "base64_encoded_image_string",
  "model_name": "symptom_classifier",
  "top_k": 3
}
```

#### Send Email Notification

```http
POST /api/v1/mcp/notification/email
```

**Request Body:**
```json
{
  "to_email": "patient@example.com",
  "subject": "Appointment Reminder",
  "body": "Your appointment is scheduled for...",
  "template_name": null
}
```

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-17T12:00:00Z",
  "services": {
    "api": "running",
    "database": "connected",
    "redis": "connected",
    "mcp": "mock"
  }
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "path": "/api/v1/endpoint"
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting

- Default: 60 requests per minute per user
- Headers returned:
  - `X-RateLimit-Limit`: Maximum requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## Interactive Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
