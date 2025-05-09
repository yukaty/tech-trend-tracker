FROM python:3.13-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK punkt tokenizer
RUN python -m nltk.downloader punkt_tab

# Copy project files
COPY . .

# Set Python path for imports
ENV PYTHONPATH=/app

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
