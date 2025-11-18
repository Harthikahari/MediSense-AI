#!/bin/bash
# Setup script for MediSense-AI development environment

set -e

echo "🚀 Setting up MediSense-AI development environment..."

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed."; exit 1; }

echo "✅ Prerequisites check passed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
else
    echo "✅ .env file already exists"
fi

# Setup Python virtual environment for local development (optional)
if [ "$1" == "--local" ]; then
    echo "🐍 Setting up Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Python environment ready"
    cd ..
fi

# Setup frontend for local development (optional)
if [ "$1" == "--local" ]; then
    echo "📦 Setting up Node.js dependencies..."
    cd frontend
    npm install
    echo "✅ Node.js environment ready"
    cd ..
fi

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/chroma
mkdir -p logs
mkdir -p backend/app/models
echo "✅ Directories created"

# Build and start Docker containers
echo "🐳 Building Docker containers..."
docker-compose build

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: docker-compose up"
echo "3. Access the application at http://localhost:3000"
echo "4. API documentation at http://localhost:8000/docs"
echo ""
echo "For local development:"
echo "  Backend: cd backend && source venv/bin/activate"
echo "  Frontend: cd frontend && npm start"
echo ""
