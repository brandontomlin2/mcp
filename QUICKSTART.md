# Quick Start Guide

## Multi-Service MCP Server Setup (Docker)

Follow these steps to get your Multi-Service MCP server running with Claude Desktop using Docker:

### 1. Prerequisites
- Docker installed and running
- Claude Desktop installed

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/brandont/multi-service-mcp-server.git
cd multi-service-mcp-server

# Run the Docker setup script
chmod +x setup-docker.sh
./setup-docker.sh
```

### 3. Configure Claude Desktop

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration (update the path to match your installation):
```json
{
  "mcpServers": {
    "multi-service": {
      "command": "/path/to/your/multi-service-mcp-server/run_mcp_docker.sh",
      "args": []
    }
  }
}
```

**Alternative**: Copy the provided config and update the path:
```bash
cp claude_desktop_config_docker.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Then edit the file to update the path
```

### 4. Restart Claude Desktop

Close and reopen Claude Desktop to load the new MCP server.

### 5. Test in Claude Desktop

Try these example prompts:
- "Search ArXiv for papers on machine learning"
- "Get details for paper 2301.00001"
- "Show me recent papers in cs.AI from the last week"
- "Advanced search: papers by Yann LeCun in cs.AI category from 2023"
- "Use sequential thinking to solve this complex problem step by step"
- "Get a summary of my current thinking session"

### 6. Troubleshooting

If something doesn't work:
1. Check that the path points to `run_mcp_docker.sh` in the config
2. Verify Docker is running: `docker --version`
3. Test the Docker container: `docker run --rm multi-service-mcp-server python test_server.py --test`
4. Make sure the wrapper script is executable: `chmod +x run_mcp_docker.sh`

## Available Tools

### ArXiv Tools
- **search_arxiv**: Search for papers by query
- **get_paper_details**: Get detailed paper information
- **get_recent_papers**: Get recent papers by category
- **get_papers_by_author**: Get papers by specific authors
- **get_trending_categories**: Get trending categories
- **advanced_search**: Multi-field search with Boolean operators
- **get_paper_by_version**: Get specific versions of papers
- **search_by_phrase**: Search for exact phrases

### Sequential Thinking Tools
- **sequential_thinking**: Dynamic problem-solving through structured thoughts
- **get_thought_summary**: Get summary of current thinking session
- **clear_thought_history**: Clear thought history and branches

That's it! You should now have Multi-Service MCP access in Claude Desktop via Docker.
