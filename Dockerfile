# Multi-stage Dockerfile for Cancrizans

# Stage 1: Builder
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy dependency files
COPY pyproject.toml README.md ./
COPY cancrizans/ ./cancrizans/

# Install dependencies
RUN uv pip install --system -e ".[dev]"

# Stage 2: Runtime
FROM python:3.11-slim

LABEL maintainer="Cancrizans Project"
LABEL description="Explore and render J.S. Bach's Crab Canon as a strict palindrome"
LABEL version="0.40.0"

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    fluidsynth \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY cancrizans/ ./cancrizans/
COPY pyproject.toml README.md ./

# Install cancrizans in editable mode
RUN pip install -e .

# Create output directory
RUN mkdir -p /output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose volume for output files
VOLUME ["/output"]

# Default command: show help
CMD ["cancrizans", "--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import cancrizans; print('OK')" || exit 1

# Examples of usage:
# Build: docker build -t cancrizans .
# Run:   docker run -v $(pwd)/output:/output cancrizans generate scale --output /output/canon.mid
# Shell: docker run -it cancrizans /bin/bash
