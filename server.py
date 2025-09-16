#!/usr/bin/env python3
"""
Multi-Service MCP Server

A Model Context Protocol server providing access to ArXiv research papers and Sequential Thinking tools.
"""

from mcp.server.fastmcp import FastMCP
from services.arxiv_service import ArXivService
from tools.arxiv_tools import ArXivToolProvider
from services.sequential_thinking_service import SequentialThinkingService
from tools.sequential_thinking_tools import SequentialThinkingToolProvider

# Create the MCP server
mcp = FastMCP("Multi-Service MCP Server")

# Initialize ArXiv service and tools
arxiv_service = ArXivService()
arxiv_tools = ArXivToolProvider(mcp, arxiv_service)

# Initialize Sequential Thinking service and tools
thinking_service = SequentialThinkingService()
thinking_tools = SequentialThinkingToolProvider(mcp, thinking_service)

if __name__ == "__main__":
    # Run the server
    mcp.run(transport='stdio')
