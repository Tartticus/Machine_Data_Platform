FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY machine1scraper.py .

# Default envs – override in compose/K8s if needed
ENV MODBUS_HOST="0.0.0.0" \
    MODBUS_PORT="5020"

EXPOSE 5020

CMD ["python", "machine1scraper.py"]