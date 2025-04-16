# FastAPI React Docker Application

A full-stack application built with FastAPI (backend), React (frontend), and PostgreSQL (database), all containerized with Docker.

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
- PostgreSQL on port 5432

## Production Setup

To build and run the production version:

```bash
docker build -t fastapi-react-app .
docker run -p 8000:8000 fastapi-react-app
```

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string

### Frontend
- `REACT_APP_API_URL`: Backend API URL

### Database
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

## Features

- FastAPI backend with automatic API documentation
- React frontend with hot-reloading in development
- PostgreSQL database with persistent storage
- Docker Compose for development environment
- Multi-stage Docker build for production
- Volume mounts for live code updates in development