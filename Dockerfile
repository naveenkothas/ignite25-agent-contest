# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Set default values if not provided\n\
export HOST=${HOST:-0.0.0.0}\n\
export PORT=${PORT:-8080}\n\
export ENTITIES_DIR=${ENTITIES_DIR:-./agents}\n\
export MODE=${MODE:-user}\n\
export AUTH_ENABLED=${AUTH_ENABLED:-true}\n\
\n\
echo "Starting Agent Framework DevUI..."\n\
echo "Host: $HOST"\n\
echo "Port: $PORT"\n\
echo "Entities Dir: $ENTITIES_DIR"\n\
echo "Mode: $MODE"\n\
echo "Auth: $AUTH_ENABLED"\n\
\n\
# Start the devui server\n\
exec devui "$ENTITIES_DIR" \\\n\
    --host "$HOST" \\\n\
    --port "$PORT" \\\n\
    --mode "$MODE" \\\n\
    $([ "$AUTH_ENABLED" = "true" ] && echo "--auth" || echo "")\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start the application
CMD ["/app/start.sh"]
