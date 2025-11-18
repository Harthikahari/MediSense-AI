# MediSense-AI

**Enterprise Clinical AI Multi-Agent Assistant**

MediSense-AI is a production-ready, multi-agent Clinical AI Assistant that provides comprehensive healthcare workflow automation with strict safety, privacy, and compliance guardrails.

## Features

- **Appointment Scheduling**: Doctor availability-aware booking with timezone support
- **Clinical Consultation Chat**: Text-based consultations backed by advanced LLM (MCP) and CrewAI orchestration
- **Symptom Image Analysis**: Medical-grade image classification and segmentation using ONNX models
- **Report Understanding**: OCR-based extraction of clinical data from PDFs and reports
- **Prescription Generation**: E-prescription drafts with validation, drug interaction checks, and provenance tracking
- **Follow-up Scheduling**: Automated follow-up appointment management
- **Payment Gateway Integration**: Sandbox payment processing with pre-authorization
- **SQL Agent**: Safe, parameterized queries to EHR/clinical databases (PostgreSQL)
- **RAG Agent**: Vector database-backed retrieval for documents and medical records
- **Routing Agent**: Intelligent intent classification and agent dispatch
- **Notification Service**: SMS and email messaging with template support
- **Guardrails**: Safety, privacy, and HIPAA-like compliance enforcement with PII/PHI redaction
- **Audit Logging**: Immutable traceability for all clinical decisions and agent actions
- **Evaluation Pipelines**: RAGAS metrics and RLHF feedback loop support

## Architecture

![System Architecture](design/diagrams/system-architecture.svg)

See [Architecture Documentation](design/architecture.md) for detailed system design.

## Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React with TypeScript
- **Agent Orchestration**: CrewAI-style multi-agent system
- **LLM**: Anthropic AI via MCP protocol
- **Vector Database**: Chroma (with Milvus/Pinecone fallback support)
- **Database**: PostgreSQL
- **Inference**: ONNX Runtime for medical image analysis
- **Background Jobs**: Celery + Redis
- **Containerization**: Docker + docker-compose
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git
- (Optional) Node.js 18+ for frontend development
- (Optional) Python 3.11+ for local backend development

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Harthikahari/MediSense-AI.git
   cd MediSense-AI
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and fill in required values (database credentials, API keys, etc.)
   ```

3. **Start the application**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend UI: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

### Seed Database

```bash
docker-compose exec db psql -U medisense -d medisense_db -f /seed_data/demo_db.sql
```

Or from your host:
```bash
psql -h localhost -U medisense -d medisense_db -f seed_data/demo_db.sql
```

## Development

### Running Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec backend pytest app/tests/test_agents.py
```

### Running RAGAS Evaluation

```bash
# Local evaluation
docker-compose exec backend python -m ragas.evaluate --config ragas/ragas_config.yaml

# CI evaluation runs automatically on push (see .github/workflows/ragas-eval.yml)
```

### Linting and Code Quality

```bash
# Run linters
docker-compose exec backend black app/
docker-compose exec backend isort app/
docker-compose exec backend flake8 app/
docker-compose exec backend mypy app/
```

## MCP Configuration

MediSense-AI supports two MCP modes:

### Mock Mode (Development)
```env
MCP_MODE=mock
```
Uses simulated MCP servers for local development and testing.

### Anthropic Mode (Production)
```env
MCP_MODE=anthropic
ANTHROPIC_API_KEY=your_api_key_here
MCP_HOST=https://api.anthropic.com
```

Replace mock MCP with real Anthropic API integration. Ensure you have valid Anthropic API credentials.

## Agent System

MediSense-AI includes the following specialized agents:

1. **Routing Agent**: Classifies user intent and dispatches to appropriate specialist agents
2. **RAG Agent**: Retrieves relevant context from vector database
3. **SQL Agent**: Safely executes parameterized database queries
4. **Appointment Booking Agent**: Manages doctor calendars and schedules
5. **Scheduling Agent**: Handles follow-up appointments
6. **Payment Gateway Agent**: Processes payments (sandbox mode)
7. **Notification Agent**: Sends email and SMS notifications
8. **Image Understanding Agent**: Analyzes symptom photos using ONNX models
9. **Report Understanding Agent**: Extracts entities from clinical PDFs
10. **Prescription Generation Agent**: Drafts validated e-prescriptions
11. **Guardrail Agent**: Enforces safety policies and redacts PHI/PII
12. **Audit Agent**: Maintains immutable audit trails

## Security & Privacy

MediSense-AI implements multiple layers of security:

- **PHI/PII Redaction**: Automatic redaction of sensitive information
- **Guardrails Engine**: Policy-based content filtering and validation
- **Audit Logging**: Immutable logs for compliance and traceability
- **Role-based Access Control**: User permissions and authorization
- **Secure Communication**: TLS/mTLS for MCP communication

See [Guardrails Documentation](docs/GUARDRAILS.md) for detailed security policies.

## RLHF Pipeline

MediSense-AI supports Reinforcement Learning from Human Feedback:

1. **Preference Collection**: UI for clinicians to rate agent responses
2. **Reward Model Training**: Scripts to train preference models
3. **PPO Fine-tuning**: Offline policy optimization

See [RLHF README](docs/RLHF_README.md) for detailed instructions.

## Deployment

### Docker Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment

```bash
kubectl apply -f infra/k8s/
```

See [Deployment Guide](docs/DEPLOYMENT.md) for production deployment instructions.

## Project Structure

```
MediSense-AI/
├── backend/          # FastAPI backend application
│   ├── app/
│   │   ├── agents/   # Agent implementations
│   │   ├── api/      # REST API routes
│   │   ├── mcp_clients/  # MCP protocol clients
│   │   ├── models/   # Database models
│   │   ├── services/ # Business logic services
│   │   └── core/     # Core utilities (config, security, logging)
│   └── Dockerfile
├── frontend/         # React TypeScript frontend
├── design/          # Architecture documentation and diagrams
├── seed_data/       # Demo data for testing
├── ragas/           # Evaluation configurations
├── ci/              # GitHub Actions workflows
└── docs/            # Additional documentation
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Support

For issues and questions:
- GitHub Issues: https://github.com/Harthikahari/MediSense-AI/issues
- Documentation: [docs/](docs/)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Agent orchestration inspired by [CrewAI](https://github.com/joaomdmoura/crewAI)
- LLM integration via [Anthropic](https://www.anthropic.com/)
- Evaluation powered by [RAGAS](https://github.com/explodinggradients/ragas)

---

**Disclaimer**: MediSense-AI is a demonstration system for educational and research purposes. It is not intended for actual clinical use without proper validation, regulatory approval, and clinical oversight.