FROM python:3.11-slim

# System deps for weasyprint (optional PDF export)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
    libffi-dev libcairo2 libglib2.0-0 shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

COPY server.py export.py config.py setup_wizard.py ./
COPY config.example.json ./

RUN mkdir -p data

EXPOSE 8765

VOLUME ["/app/data"]

ENV ASF_WORKSPACE_PATH=/app/data

CMD ["python3", "server.py"]
