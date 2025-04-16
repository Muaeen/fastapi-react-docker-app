# FastAPI React Docker Application

A full-stack application built with FastAPI (backend) and React (frontend), containerized with Docker.

## Project Structure

```
.
├── backend/             # FastAPI backend
├── frontend/           # React frontend
├── Dockerfile          # Production multi-stage build
└── docker-compose.yml  # Development setup
```

## Development Setup

To run the application in development mode:

```bash
docker-compose up --build
```

This will start:
- Frontend on http://localhost:3000
- Backend on http://localhost:8000

## Production Setup

To build and run the production version:

```bash
docker build -t fastapi-react-app .
docker run -p 8000:8000 -p 3000:3000 fastapi-react-app
```

## Environment Variables

### Frontend
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

## Features

- FastAPI backend with automatic API documentation
- React frontend with hot-reloading in development
- Docker Compose for development environment
- Multi-stage Docker build for production
- Volume mounts for live code updates in development