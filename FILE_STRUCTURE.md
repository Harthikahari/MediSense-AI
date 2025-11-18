# MediSense-AI - Complete File Structure

This document provides a comprehensive overview of the MediSense-AI repository structure.

## Repository Root

```
MediSense-AI/
├── README.md                      # Main project documentation
├── LICENSE                        # Apache 2.0 license
├── CONTRIBUTING.md                # Contribution guidelines
├── SECURITY.md                    # Security policy
├── CHANGELOG.md                   # Version history
├── CODE_OF_CONDUCT.md            # Community guidelines
├── Makefile                       # Common commands
├── .gitignore                     # Git ignore patterns
├── .editorconfig                  # Editor configuration
├── .env.example                   # Environment variables template
├── .env.production.example        # Production environment template
├── docker-compose.yml             # Docker Compose configuration
├── requirements.txt               # Python dependencies
└── FILE_STRUCTURE.md             # This file
```

## Backend Directory

```
backend/
├── Dockerfile                     # Backend container definition
├── .dockerignore                  # Docker build exclusions
│
├── app/
│   ├── __init__.py               # Application package
│   ├── main.py                   # FastAPI application entry point
│   │
│   ├── core/                     # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py             # Settings and configuration
│   │   ├── logger.py             # Logging and audit setup
│   │   └── security.py           # Security utilities (JWT, PHI redaction)
│   │
│   ├── db/                       # Database layer
│   │   ├── __init__.py
│   │   ├── base.py               # Database connection and session
│   │   ├── crud.py               # CRUD operations
│   │   └── schemas.py            # Pydantic schemas for validation
│   │
│   ├── models/                   # Database models
│   │   ├── __init__.py
│   │   ├── user.py               # User model
│   │   ├── appointment.py        # Appointment model
│   │   └── audit.py              # Audit log models
│   │
│   ├── agents/                   # AI Agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Base agent class
│   │   ├── routing_agent.py      # Intent classification
│   │   ├── rag_agent.py          # Document retrieval
│   │   ├── sql_agent.py          # Safe database queries
│   │   ├── appointment_agent.py  # Appointment management
│   │   ├── payment_agent.py      # Payment processing
│   │   ├── image_agent.py        # Image analysis
│   │   ├── report_agent.py       # Report processing
│   │   ├── prescription_agent.py # Prescription generation
│   │   ├── guardrail_agent.py    # Safety enforcement
│   │   └── audit_agent.py        # Provenance tracking
│   │
│   ├── mcp_clients/              # MCP protocol clients
│   │   ├── __init__.py
│   │   ├── mcp_base.py           # Base MCP client interface
│   │   ├── mcp_document.py       # Document operations
│   │   ├── mcp_db.py             # Database operations
│   │   ├── mcp_model.py          # ML model inference
│   │   ├── mcp_payment.py        # Payment gateway
│   │   └── mcp_notification.py   # Email/SMS notifications
│   │
│   ├── api/                      # REST API routes
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── routes_auth.py    # Authentication endpoints
│   │       ├── routes_agents.py  # Agent orchestration endpoints
│   │       └── routes_mcp.py     # Direct MCP access
│   │
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── embedding_service.py  # Text embeddings
│   │   ├── vector_db.py          # Vector database (Chroma)
│   │   └── onnx_inference.py     # ONNX model inference
│   │
│   └── tests/                    # Test suite
│       ├── __init__.py
│       ├── test_agents.py        # Agent tests
│       └── test_endpoints.py     # API endpoint tests
```

## Frontend Directory

```
frontend/
├── Dockerfile                     # Frontend container definition
├── .dockerignore                  # Docker build exclusions
├── README.md                      # Frontend documentation
├── package.json                   # Node.js dependencies
├── tsconfig.json                  # TypeScript configuration
│
├── public/
│   └── index.html                # HTML template
│
└── src/
    ├── App.tsx                   # Main application component
    ├── App.css                   # Application styles
    ├── index.tsx                 # Application entry point
    └── index.css                 # Global styles
```

## Infrastructure Directory

```
infra/
├── k8s/                          # Kubernetes manifests
│   ├── deployment.yaml           # Deployment configuration
│   └── service.yaml              # Service definitions
│
└── terraform/                    # Terraform (IaC) - for future use
```

## CI/CD Directory

```
.github/
└── workflows/
    ├── python-tests.yml          # Backend CI pipeline
    └── ragas-eval.yml            # Evaluation pipeline
```

## Documentation Directory

```
docs/
├── MCP_API_SPEC.md               # MCP protocol specification
├── GUARDRAILS.md                 # Safety and compliance docs
├── RLHF_README.md                # RLHF training guide
├── API.md                        # REST API documentation
└── DEPLOYMENT.md                 # Deployment instructions
```

## Design Directory

```
design/
├── architecture.md               # System architecture documentation
└── diagrams/                     # Architecture diagrams (SVG/PNG)
```

## Evaluation Directory

```
ragas/
├── ragas_config.yaml             # RAGAS evaluation config
└── testset.jsonl                 # Test dataset (50 examples)
```

## Seed Data Directory

```
seed_data/
├── demo_db.sql                   # Database seed script
├── sample_reports/               # Sample PDF reports (to be added)
└── sample_images/                # Sample medical images (to be added)
```

## Scripts Directory

```
scripts/
├── setup.sh                      # Development environment setup
├── test.sh                       # Test execution script
└── deploy.sh                     # Deployment automation
```

## File Count Summary

| Category | Count | Description |
|----------|-------|-------------|
| **Backend Python Files** | 40+ | Core application, agents, services |
| **Frontend TypeScript** | 8 | React components and configuration |
| **Configuration Files** | 15+ | Docker, CI/CD, environment |
| **Documentation** | 10+ | Guides, specifications, README files |
| **Infrastructure** | 5+ | Kubernetes, deployment manifests |
| **Test Files** | 5+ | Unit tests, integration tests |
| **Scripts** | 3 | Automation and setup |
| **Total Files** | **85+** | Complete repository |

## Key Features by Directory

### Backend (`backend/app/`)
- **11 Specialized Agents** for different clinical tasks
- **5 MCP Clients** for external service integration
- **Complete API Layer** with authentication and routing
- **Database Models** with SQLAlchemy ORM
- **Security Layer** with JWT and PHI redaction
- **Test Coverage** with pytest

### Frontend (`frontend/src/`)
- **React 18** with TypeScript
- **Authentication UI** (login/register)
- **Chat Interface** for agent interaction
- **Responsive Design** with CSS

### Infrastructure (`infra/`)
- **Kubernetes Manifests** for cloud deployment
- **Docker Compose** for local development
- **CI/CD Pipelines** with GitHub Actions

### Documentation (`docs/`)
- **API Documentation** with examples
- **Architecture Diagrams** and explanations
- **Deployment Guides** for multiple platforms
- **Security Policies** and compliance info

## Technology Stack

| Component | Technology | Files |
|-----------|-----------|-------|
| Backend Framework | FastAPI | `app/main.py`, `app/api/` |
| Frontend Framework | React + TypeScript | `frontend/src/` |
| Database | PostgreSQL | `app/models/`, `app/db/` |
| Vector DB | Chroma | `app/services/vector_db.py` |
| Cache/Queue | Redis + Celery | `docker-compose.yml` |
| ML Inference | ONNX Runtime | `app/services/onnx_inference.py` |
| Authentication | JWT | `app/core/security.py` |
| Testing | pytest, Jest | `app/tests/` |
| CI/CD | GitHub Actions | `.github/workflows/` |
| Containerization | Docker | `Dockerfile`, `docker-compose.yml` |
| Orchestration | Kubernetes | `infra/k8s/` |

## Quick Navigation

### For Developers
- Start here: [CONTRIBUTING.md](CONTRIBUTING.md)
- Setup: [scripts/setup.sh](scripts/setup.sh)
- Tests: [backend/app/tests/](backend/app/tests/)

### For Deployers
- Deployment: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- Configuration: [.env.example](.env.example)
- Kubernetes: [infra/k8s/](infra/k8s/)

### For Users
- API Docs: [docs/API.md](docs/API.md)
- Architecture: [design/architecture.md](design/architecture.md)
- Security: [SECURITY.md](SECURITY.md)

## File Size Estimates

| Directory | Estimated Size | Content |
|-----------|---------------|---------|
| `backend/` | ~500 KB | Python source code |
| `frontend/` | ~100 KB | TypeScript/React code |
| `node_modules/` | ~200 MB | Node dependencies (gitignored) |
| `venv/` | ~300 MB | Python virtual env (gitignored) |
| `docs/` | ~200 KB | Documentation |
| `infra/` | ~50 KB | Infrastructure configs |
| **Total (repo)** | **~1 MB** | Excluding dependencies |

## Adding New Files

When adding new components, follow this structure:

### New Agent
```
backend/app/agents/new_agent.py
backend/app/tests/test_new_agent.py
docs/agents/new_agent.md (optional)
```

### New API Endpoint
```
backend/app/api/v1/routes_new.py
backend/app/tests/test_routes_new.py
docs/API.md (update)
```

### New Service
```
backend/app/services/new_service.py
backend/app/tests/test_new_service.py
```

## Maintenance

### Files to Update Regularly
- `CHANGELOG.md` - On each release
- `requirements.txt` - When dependencies change
- `package.json` - When frontend deps change
- `docs/API.md` - When API changes
- `.env.example` - When new config added

### Files to Review
- `SECURITY.md` - Quarterly
- `CONTRIBUTING.md` - When process changes
- `README.md` - Keep up to date

---

**Last Updated**: 2025-01-17
**Version**: 1.0.0
**Total Files**: 85+
**Lines of Code**: ~15,000+
