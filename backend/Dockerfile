FROM python:3.11-slim

WORKDIR /app

# Install build essentials if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy source tree
COPY backend ./backend
COPY scripts ./scripts

# Set Python module search path
ENV PYTHONPATH=/app/backend

# Default entrypoint runs the research workflow CLI
CMD ["python", "scripts/run_research_cli.py"]
