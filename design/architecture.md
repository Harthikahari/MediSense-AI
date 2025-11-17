# MediSense-AI Architecture

## System Overview

MediSense-AI is an enterprise-grade, multi-agent Clinical AI Assistant built on a modern microservices architecture with strict safety, privacy, and compliance guardrails.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│                    (React TypeScript SPA)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTPS/REST
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                      API Gateway Layer                       │
│                        (FastAPI)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐ │
│  │   Auth   │  │ Agents   │  │         MCP API          │ │
│  │ Endpoints│  │Endpoints │  │      Endpoints           │ │
│  └──────────┘  └──────────┘  └──────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────┴───────┐ ┌──┴───────┐ ┌──┴──────────┐
│ Agent         │ │   MCP    │ │  Services   │
│ Orchestration │ │ Clients  │ │   Layer     │
└───────────────┘ └──────────┘ └─────────────┘
```

## Core Components

### 1. Frontend Layer
- **Technology**: React 18 with TypeScript
- **Features**:
  - User authentication
  - Chat interface for agent interaction
  - Real-time response display
  - File upload for image/document analysis
- **Communication**: REST API over HTTPS

### 2. API Gateway (FastAPI)
- **Routes**:
  - `/api/v1/auth/*` - Authentication endpoints
  - `/api/v1/agents/*` - Agent orchestration endpoints
  - `/api/v1/mcp/*` - Direct MCP client access
- **Middleware**:
  - CORS handling
  - JWT authentication
  - Rate limiting
  - Request logging

### 3. Agent Orchestration Layer

#### Multi-Agent System
MediSense-AI implements a CrewAI-inspired multi-agent architecture:

```
┌────────────────┐
│ Routing Agent  │ ◄─── User Query
└────────┬───────┘
         │
         │ Routes to specialist
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│  RAG  │ │Appoint- │
│ Agent │ │ment     │
└───────┘ │Agent    │
          └─────────┘
```

#### Agent Types

1. **Routing Agent**
   - Classifies user intent
   - Routes to specialist agents
   - Confidence scoring

2. **RAG Agent**
   - Document retrieval from vector DB
   - Context assembly
   - LLM-based answer generation

3. **SQL Agent**
   - NL to SQL translation
   - Safe, parameterized query execution
   - Read-only database access

4. **Appointment Agent**
   - Calendar management
   - Availability checking
   - Double-booking prevention
   - Payment integration

5. **Image Agent**
   - ONNX model inference
   - Symptom classification
   - Lesion segmentation

6. **Report Agent**
   - OCR processing
   - Structured data extraction
   - Entity recognition

7. **Prescription Agent**
   - Medication recommendation
   - Drug interaction checking
   - Contraindication validation

8. **Guardrail Agent**
   - PHI/PII redaction
   - Safety policy enforcement
   - Content filtering

9. **Audit Agent**
   - Immutable logging
   - Provenance tracking
   - Explainability

10. **Payment Agent**
    - Payment processing
    - Pre-authorization
    - Refund handling

### 4. MCP (Model Context Protocol) Layer

Abstraction layer for external service integration:

- **Document MCP**: Document search, OCR, PDF processing
- **Database MCP**: Safe SQL execution
- **Model MCP**: ONNX inference
- **Payment MCP**: Payment gateway integration
- **Notification MCP**: Email and SMS

**Modes**:
- `mock`: Simulated responses for development
- `anthropic`: Production Claude API integration

### 5. Data Layer

#### PostgreSQL Database
```sql
Tables:
- users (authentication, roles)
- appointments (scheduling)
- audit_logs (compliance tracking)
- guardrail_violations (policy enforcement)
```

#### Chroma Vector Database
- Document embeddings
- Semantic search
- RAG context retrieval

#### Redis Cache
- Session management
- Celery task queue
- Rate limiting

### 6. Background Processing (Celery)
- Async notification sending
- Scheduled report generation
- Batch processing tasks

## Security Architecture

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Roles: admin, clinician, patient, staff

### PHI/PII Protection
- Automatic redaction using regex patterns
- Guardrail enforcement pipeline
- Encrypted data at rest and in transit

### Compliance
- HIPAA-like audit logging
- Immutable audit trails
- Data access tracking

## Data Flow

### Typical Request Flow

```
1. User Query → Frontend
2. Frontend → API Gateway (with JWT)
3. API Gateway → Routing Agent
4. Routing Agent → Specialist Agent (e.g., RAG Agent)
5. Specialist Agent → MCP Client (e.g., Document MCP)
6. MCP Client → External Service / DB
7. Response ← External Service
8. Response ← MCP Client
9. Response ← Specialist Agent
10. Response → Guardrail Agent (validation)
11. Safe Response → API Gateway
12. Response → Frontend
```

### Audit Trail

Every step is logged:
- Agent decisions
- LLM API calls
- Data access
- Policy violations

## Deployment Architecture

### Development
```
docker-compose:
  - backend
  - frontend
  - postgres
  - redis
  - celery worker
  - celery beat
```

### Production (Kubernetes)
```
Pods:
  - Backend (3 replicas)
  - Frontend (2 replicas)
  - Celery Workers (5 replicas)
  - PostgreSQL (StatefulSet)
  - Redis (StatefulSet)

Services:
  - LoadBalancer (frontend)
  - ClusterIP (backend, db, redis)
```

## Scalability

- **Horizontal Scaling**: Backend pods can scale based on CPU/memory
- **Database**: PostgreSQL with read replicas
- **Caching**: Redis for frequently accessed data
- **Async Processing**: Celery for long-running tasks

## Monitoring & Observability

- **Logs**: Structured logging (JSON)
- **Metrics**: Prometheus-compatible endpoints
- **Tracing**: Distributed tracing for agent calls
- **Health Checks**: `/health` endpoint with service status

## Evaluation Pipeline (RAGAS)

```
Nightly evaluation:
1. Load test dataset
2. Run queries through agent system
3. Calculate metrics:
   - Context precision
   - Context recall
   - Faithfulness
   - Answer relevancy
4. Generate report
5. Alert on threshold violations
```

## Future Enhancements

1. **RLHF Pipeline**: Collect human feedback, train reward models
2. **Real-time Collaboration**: WebSocket support for live consultations
3. **Mobile Apps**: Native iOS/Android applications
4. **Voice Interface**: Speech-to-text and text-to-speech integration
5. **Multi-language**: Support for international deployments
6. **Advanced Analytics**: ML-powered insights dashboard

## Technology Stack Summary

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React 18 (TypeScript)
- **Database**: PostgreSQL 15
- **Vector DB**: Chroma
- **Cache**: Redis 7
- **Task Queue**: Celery
- **ML Inference**: ONNX Runtime
- **LLM**: Claude (Anthropic)
- **Container**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions

---

**Version**: 1.0.0
**Last Updated**: 2025-01-17
