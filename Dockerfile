# Build frontend
FROM node:16-alpine as frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Build backend
FROM python:3.10 as backend
WORKDIR /app

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend files to backend static directory
COPY --from=frontend-build /frontend/build /app/static

# Final image
FROM node:16-alpine

# Set up frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

# Copy backend from backend stage
COPY --from=backend /app /backend
COPY --from=backend /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=backend /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Expose ports
EXPOSE 3000 8000

# Run both services
CMD ["sh", "-c", "cd /frontend && npm start & cd /backend && uvicorn main:app --host 0.0.0.0 --port 8000"]