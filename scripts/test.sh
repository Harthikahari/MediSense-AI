#!/bin/bash
# Run tests for MediSense-AI

set -e

echo "🧪 Running MediSense-AI tests..."

# Run backend tests
echo "🐍 Running backend tests..."
docker-compose exec -T backend pytest app/tests/ -v --cov=app --cov-report=term-missing

# Run frontend tests (if frontend is running)
if docker-compose ps | grep -q frontend; then
    echo "⚛️  Running frontend tests..."
    docker-compose exec -T frontend npm test -- --watchAll=false
fi

echo "✅ All tests passed!"
