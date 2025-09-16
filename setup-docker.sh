# Multi-Service MCP Server Docker Setup Script

echo "🐳 Setting up Multi-Service MCP Server with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker is installed"

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t multi-service-mcp-server .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Test the container
echo "🧪 Testing the MCP server..."
docker run --rm multi-service-mcp-server python test_server.py --test

if [ $? -eq 0 ]; then
    echo "✅ MCP server test passed"
else
    echo "❌ MCP server test failed"
    exit 1
fi

echo ""
echo "🎉 Docker setup complete!"
echo ""
echo "To run the MCP server:"
echo "  docker run -it multi-service-mcp-server"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up"
echo ""
echo "For Claude Desktop integration, you'll need to:"
echo "1. Create a wrapper script that runs the Docker container"
echo "2. Update your Claude Desktop config to use the wrapper script"
echo ""
echo "Example wrapper script (create 'run_mcp.sh'):"
echo "#!/bin/bash"
echo "docker run -i multi-service-mcp-server"
echo ""
echo "Then make it executable: chmod +x run_mcp.sh"
