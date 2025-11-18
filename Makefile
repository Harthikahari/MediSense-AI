# MediSense-AI Makefile

.PHONY: help setup start stop restart logs test clean build deploy

help: ## Show this help message
	@echo "MediSense-AI - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment
	@bash scripts/setup.sh

setup-local: ## Setup local development environment (with venv)
	@bash scripts/setup.sh --local

start: ## Start all services
	docker-compose up -d

stop: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## View logs from all services
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

test: ## Run all tests
	@bash scripts/test.sh

test-backend: ## Run backend tests only
	docker-compose exec backend pytest app/tests/ -v

test-coverage: ## Run tests with coverage report
	docker-compose exec backend pytest app/tests/ --cov=app --cov-report=html
	@echo "Coverage report: backend/htmlcov/index.html"

lint: ## Run linters
	docker-compose exec backend black app/ --check
	docker-compose exec backend flake8 app/
	docker-compose exec backend mypy app/ --ignore-missing-imports

format: ## Format code
	docker-compose exec backend black app/
	docker-compose exec backend isort app/

build: ## Build Docker images
	docker-compose build

clean: ## Clean up containers and volumes
	docker-compose down -v
	rm -rf data/chroma/*
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

db-migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

db-seed: ## Seed database with demo data
	docker-compose exec db psql -U medisense -d medisense_db -f /seed_data/demo_db.sql

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-db: ## Open PostgreSQL shell
	docker-compose exec db psql -U medisense -d medisense_db

deploy-prod: ## Deploy to production
	@bash scripts/deploy.sh production

deploy-staging: ## Deploy to staging
	@bash scripts/deploy.sh staging

docs: ## Generate documentation
	@echo "Building documentation..."
	cd docs && python -m mkdocs build

.DEFAULT_GOAL := help
