FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    libpq-dev gcc tesseract-ocr poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Increase pip timeout & retries for slow networks
RUN pip config set global.timeout 120 && \
    pip config set global.retries 10 && \
    pip config set global.default-timeout 120

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]