# FastAPI React Docker Application

A full-stack web application with FastAPI backend, React frontend, and Docker configuration.

## Project Structure

```
.
├── backend/         # FastAPI backend
├── frontend/        # React frontend
└── docker/          # Docker configuration
```

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/Muaeen/fastapi-react-docker-app.git
cd fastapi-react-docker-app
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Backend
The backend is built with FastAPI and provides a RESTful API.

### Frontend
The frontend is built with React and communicates with the backend API.

## License
MIT