FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the start script is executable
RUN chmod +x start.sh

# Create non-root user for security
RUN useradd -m appuser
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "src/main.py"] 