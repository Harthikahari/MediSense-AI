# Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud Providers](#cloud-providers)
6. [Environment Configuration](#environment-configuration)
7. [Database Setup](#database-setup)
8. [Monitoring](#monitoring)
9. [Backup & Recovery](#backup--recovery)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum:**
- 4 CPU cores
- 8 GB RAM
- 50 GB disk space
- Ubuntu 20.04+ or equivalent

**Recommended:**
- 8 CPU cores
- 16 GB RAM
- 100 GB SSD storage
- Ubuntu 22.04 LTS

### Software Requirements

- Docker 24.0+
- Docker Compose 2.0+
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

## Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/Harthikahari/Harikrishnan.git
cd Harikrishnan

# Setup environment
make setup

# Edit .env file
nano .env

# Start services
make start

# View logs
make logs
```

### Manual Setup

```bash
# Copy environment file
cp .env.example .env

# Edit configuration
vim .env

# Build containers
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# Seed database
make db-seed
```

## Docker Deployment

### Development

```bash
docker-compose up --build
```

### Production

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or use make command
make deploy-prod
```

### Environment Variables

Create `.env` file with production values:

```bash
ENV=production
MCP_MODE=anthropic
ANTHROPIC_API_KEY=your_api_key
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.25+)
- kubectl configured
- Helm 3+ (optional)

### Deployment Steps

```bash
# Create namespace
kubectl create namespace medisense

# Create secrets
kubectl create secret generic medisense-secrets \
  --from-literal=database-url="postgresql://..." \
  --from-literal=anthropic-api-key="sk-..." \
  -n medisense

# Deploy application
kubectl apply -f infra/k8s/ -n medisense

# Check deployment
kubectl get pods -n medisense
kubectl get services -n medisense

# View logs
kubectl logs -f deployment/medisense-backend -n medisense
```

### Scaling

```bash
# Scale backend
kubectl scale deployment medisense-backend --replicas=5 -n medisense

# Auto-scaling
kubectl autoscale deployment medisense-backend \
  --min=2 --max=10 --cpu-percent=70 -n medisense
```

## Cloud Providers

### AWS EKS

```bash
# Create EKS cluster
eksctl create cluster --name medisense-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.large \
  --nodes 3

# Deploy application
kubectl apply -f infra/k8s/
```

### Google GKE

```bash
# Create GKE cluster
gcloud container clusters create medisense-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-4

# Deploy application
kubectl apply -f infra/k8s/
```

### Azure AKS

```bash
# Create AKS cluster
az aks create \
  --resource-group medisense-rg \
  --name medisense-cluster \
  --node-count 3 \
  --node-vm-size Standard_D4s_v3

# Deploy application
kubectl apply -f infra/k8s/
```

## Environment Configuration

### Required Variables

```bash
# Application
ENV=production
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
POSTGRES_USER=medisense
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=medisense_db

# Redis
REDIS_URL=redis://host:6379/0

# MCP
MCP_MODE=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Security
JWT_SECRET=random_secret_key_here
SECRET_KEY=another_random_key
```

### Optional Variables

See `.env.example` for complete list.

## Database Setup

### PostgreSQL

#### Using Docker

```bash
docker-compose up -d db
```

#### Standalone Installation

```bash
# Install PostgreSQL
sudo apt-get install postgresql-15

# Create database
sudo -u postgres createdb medisense_db
sudo -u postgres createuser medisense

# Grant permissions
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE medisense_db TO medisense;"
```

#### Migrations

```bash
# Run migrations
make db-migrate

# Or manually
docker-compose exec backend alembic upgrade head
```

#### Seed Data

```bash
make db-seed
```

### Redis

```bash
# Using Docker
docker-compose up -d redis

# Or install standalone
sudo apt-get install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

## Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Database health
docker-compose exec db pg_isready

# Redis health
docker-compose exec redis redis-cli ping
```

### Logs

```bash
# All services
make logs

# Specific service
docker-compose logs -f backend

# Kubernetes
kubectl logs -f deployment/medisense-backend
```

### Metrics (Prometheus)

```yaml
# Add to deployment
- name: metrics
  containerPort: 9090
```

## Backup & Recovery

### Database Backup

```bash
# Backup
docker-compose exec db pg_dump -U medisense medisense_db > backup.sql

# Restore
docker-compose exec -T db psql -U medisense medisense_db < backup.sql
```

### Automated Backups

Add to cron:
```bash
0 2 * * * /path/to/backup-script.sh
```

## Troubleshooting

### Common Issues

#### Database Connection Failed

```bash
# Check database is running
docker-compose ps db

# Check logs
docker-compose logs db

# Test connection
docker-compose exec backend python -c "from app.db import SessionLocal; SessionLocal()"
```

#### Frontend Can't Connect to Backend

- Check CORS settings in `.env`
- Verify `REACT_APP_API_URL` in frontend
- Check network connectivity

#### High Memory Usage

```bash
# Check resource usage
docker stats

# Adjust limits in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Debug Mode

```bash
# Enable debug logging
docker-compose exec backend bash
export LOG_LEVEL=DEBUG
python -m app.main
```

## Security Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS/TLS
- [ ] Set secure JWT_SECRET
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] API rate limiting
- [ ] Input validation

## Performance Tuning

### Database

```sql
-- Add indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_appointments_date ON appointments(scheduled_start);
```

### Caching

- Enable Redis caching
- Configure cache TTL
- Use CDN for static assets

### Load Balancing

```nginx
upstream backend {
  server backend1:8000;
  server backend2:8000;
  server backend3:8000;
}
```

## Support

For deployment issues:
- GitHub Issues: https://github.com/Harthikahari/Harikrishnan/issues
- Documentation: https://github.com/Harthikahari/Harikrishnan/tree/main/docs
- Email: support@medisense-ai.example.com
