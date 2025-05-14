# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install netcat for wait script
RUN apt-get update && \
apt-get install -y netcat-openbsd && \
rm -rf /var/lib/apt/lists/*

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Copy wait script and make it executable
COPY ./wait-for-mysql.sh .
RUN chmod +x wait-for-mysql.sh

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8000"]