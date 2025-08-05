# ###########################################################################################################
# backend/Dockerfile
#
# This file contains the Dockerfile for the backend of the application.
# It uses the python:3.11-slim image.
# It installs the dependencies from the requirements.txt file.
# It copies the source code from the current directory to the /app directory.
# It exposes the port 8000.
# It starts the application using the uvicorn command.
# ###########################################################################################################
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Set Python path
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
