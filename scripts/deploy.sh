#!/bin/bash
# Deployment script for MediSense-AI

set -e

ENV=${1:-production}

echo "🚀 Deploying MediSense-AI to $ENV environment..."

if [ "$ENV" == "production" ]; then
    # Production deployment
    echo "📦 Building production images..."
    docker-compose -f docker-compose.prod.yml build

    echo "🚢 Pushing images to registry..."
    # Add your registry push commands here

    echo "☸️  Deploying to Kubernetes..."
    kubectl apply -f infra/k8s/

    echo "✅ Production deployment complete!"

elif [ "$ENV" == "staging" ]; then
    echo "🏗️  Deploying to staging..."
    # Add staging deployment commands

else
    echo "❌ Unknown environment: $ENV"
    echo "Usage: ./deploy.sh [production|staging]"
    exit 1
fi
