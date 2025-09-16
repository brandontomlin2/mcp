#!/bin/bash
# Wrapper script to run Multi-Service MCP Server in Docker for Claude Desktop

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Docker container with stdio for MCP communication
docker run -i --rm \
    -v "$SCRIPT_DIR:/app" \
    -w /app \
    multi-service-mcp-server
