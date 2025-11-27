# Use the official Python image from the Docker Hub
# Note: I used python:3.13-slim as the base image. However, it was developed on 3.13.6
# Prefered slim version to reduce image size
FROM python:3.13-slim

# Labels for metadata
# Email is a placeholder, as I haven't set up a developer website yet
LABEL maintainer="contact@srzafkiell.dev"
LABEL description="WEC Backend Technical Challenge - FastAPI Application"
LABEL version="1.0.0"

# Set environment variables
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures that Python output is sent straight to terminal (e.g., for logging)
ENV PYTHONUNBUFFERED 1
# Disable pip cache to reduce image size
ENV PIP_NO_CACHE_DIR=1
# Disable pip version check to speed up installations
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8080 for the FastAPI application
EXPOSE 8080

# Health check to ensure the application is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]