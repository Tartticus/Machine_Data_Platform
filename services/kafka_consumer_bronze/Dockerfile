FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY postgres_upload.py .

ENV POSTGRES_HOST="postgres" \
    POSTGRES_PORT="5432" \
    POSTGRES_DB="machines" \
    POSTGRES_USER="postgres" \
    POSTGRES_PASSWORD="postgres"


CMD ["python", "postgres_upload.py"]