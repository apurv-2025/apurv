# Multi-stage build for Agentic Core
FROM node:18-alpine AS frontend-builder

# Set working directory
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Build frontend
RUN npm run build

# Python backend stage
FROM python:3.11-slim AS backend-builder

# Set working directory
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./

# Build backend
RUN python setup.py build

# Final stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NODE_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend source code
COPY --from=backend-builder /app/agentic_core ./agentic_core
COPY --from=backend-builder /app/build ./build

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy configuration files
COPY backend/config ./config
COPY backend/alembic.ini ./
COPY backend/migrations ./migrations

# Copy entry point script
COPY scripts/start.sh ./start.sh
RUN chmod +x ./start.sh

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/uploads

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["./start.sh"] 