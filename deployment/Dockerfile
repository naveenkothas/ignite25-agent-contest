FROM python:3.11-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements in stages to handle dependencies better
COPY requirements-core.txt .
COPY requirements-agent.txt .

# Install core dependencies first
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-core.txt

# Then install agent framework with pre-release flag
RUN pip install --no-cache-dir --pre -r requirements-agent.txt

COPY . .

RUN groupadd -r appgroup && useradd -r -g appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

CMD ["python", "enhanced_agentic_ai_voice_demo.py"]