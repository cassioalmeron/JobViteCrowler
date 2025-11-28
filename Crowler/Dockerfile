# Multi-stage build for Python Selenium web scraper
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies required for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create output directories
RUN mkdir -p /app/jobs

# Copy project files
COPY pyproject.toml .
COPY crowler.py .
COPY main.py .
COPY ftptransfer.py .
COPY service_manager.py .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Production stage
FROM base AS production

WORKDIR /app

# Set Chrome driver path for container
ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver

# Run the main service (background job sync)
CMD ["python", "main.py"]

# Development stage
FROM base AS development

WORKDIR /app

ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver

# Keep container running for development
CMD ["tail", "-f", "/dev/null"]
