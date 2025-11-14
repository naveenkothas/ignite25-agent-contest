#!/bin/bash
set -e

# Azure App Service startup script for Agent Framework
echo "=== Azure App Service - Agent Framework Startup ==="

# Set default values if not provided by Azure App Service
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8080}
export ENTITIES_DIR=${ENTITIES_DIR:-./agents}
export MODE=${MODE:-user}
export AUTH_ENABLED=${AUTH_ENABLED:-true}

# Log environment information
echo "Environment Configuration:"
echo "- Host: $HOST"
echo "- Port: $PORT"
echo "- Entities Directory: $ENTITIES_DIR"
echo "- Mode: $MODE"
echo "- Authentication: $AUTH_ENABLED"
echo "- Python Version: $(python --version)"
echo "- Working Directory: $(pwd)"

# Ensure agents directory exists
if [ ! -d "$ENTITIES_DIR" ]; then
    echo "Creating agents directory: $ENTITIES_DIR"
    mkdir -p "$ENTITIES_DIR"
fi

# List available agents
echo "Available agents:"
find "$ENTITIES_DIR" -name "*.py" -o -name "*.yaml" | head -10

# Install any additional requirements if they exist
if [ -f "requirements.txt" ]; then
    echo "Installing/updating Python dependencies..."
    pip install --no-cache-dir -r requirements.txt
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Set up logging
export PYTHONUNBUFFERED=1

echo "Starting Agent Framework DevUI server..."

# Build the command with conditional auth flag
CMD="devui $ENTITIES_DIR --host $HOST --port $PORT --mode $MODE"

if [ "$AUTH_ENABLED" = "true" ]; then
    CMD="$CMD --auth"
fi

echo "Executing command: $CMD"

# Start the server
exec $CMD
