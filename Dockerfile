FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (required for llama-cpp-python build)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
# Note: We install llama-cpp-python with specific flags if GPU support is needed, 
# but for generic CPU docker, this is sufficient.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data and models
RUN mkdir -p data/source_docs data/vector_store models

# Expose ports
EXPOSE 8000 8501

# Script to run both API and UI
COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
