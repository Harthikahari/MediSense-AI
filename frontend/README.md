# MediSense-AI Frontend

React TypeScript frontend for MediSense-AI Clinical AI Assistant.

## Getting Started

### Development

```bash
npm install
npm start
```

The app will run at http://localhost:3000

### Build

```bash
npm run build
```

### Docker

```bash
docker build -t medisense-frontend .
docker run -p 3000:80 medisense-frontend
```

## Features

- User authentication
- Chat interface with AI agents
- Automatic agent routing
- Response display with confidence scores
- Feature overview

## Environment Variables

Create a `.env` file:

```
REACT_APP_API_URL=http://localhost:8000
```

## Architecture

The frontend communicates with the FastAPI backend to:
- Authenticate users
- Send chat queries to the agent orchestration system
- Display agent responses with provenance information
