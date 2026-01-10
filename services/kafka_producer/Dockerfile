# Use a slim Python base image
FROM python:3.11-slim

# Avoid Python writing .pyc and using buffered stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps if needed (ca-certificates, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements and install deps
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual scraper code
COPY kafka_producer.py .

# Environment variables (can be overridden at runtime)
ENV KAFKA_BOOTSTRAP_SERVERS="kafka:29092" \
    KAFKA_TOPIC="machine_events" \
    MODBUS_HOST="modbus-sim" \
    MODBUS_PORT="5020"

# Default command: run the scraper
CMD ["python", "kafka_producer.py"]
