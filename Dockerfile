# Multi-stage build optimized for Render

# Build frontend
FROM node:16-alpine as frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
# Use relative paths for API calls in production
ENV REACT_APP_API_URL=""
RUN npm run build

# Build backend
FROM python:3.10-slim as backend-build
WORKDIR /app

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Final image - combine frontend and backend
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies from backend build
COPY --from=backend-build /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=backend-build /usr/local/bin /usr/local/bin

# Copy backend code
COPY --from=backend-build /app /app

# Create a directory for static files
RUN mkdir -p /app/static

# Copy built frontend files to backend static directory
COPY --from=frontend-build /frontend/build/ /app/static/

# Install debugging tools
RUN apt-get update && apt-get install -y curl net-tools && apt-get clean

# Set environment variables for Render
ENV PORT=10000
ENV PYTHONUNBUFFERED=1

# Create a debug script
RUN echo '#!/bin/bash\necho "Static directory contents:"\nls -la /app/static\necho "Process list:"\nps aux\necho "Listening ports:"\nnetstat -tulpn' > /app/debug.sh && chmod +x /app/debug.sh

# Expose port that Render will use
EXPOSE $PORT

# Start command for Render
CMD uvicorn main:app --host 0.0.0.0 --port $PORT