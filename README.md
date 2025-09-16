# Multi-Service MCP Server

A modular Model Context Protocol (MCP) server that provides scaled access to ArXiv research papers and Sequential Thinking tools for Claude Desktop applications.

## 🏗️ **Architecture**

This server uses a clean, modular architecture with tools organized in separate folders:

```
/Users/brandont/git/mpc/
├── server.py                           # Main server file
├── services/                           # Business logic
│   ├── arxiv_service.py               # ArXiv API operations
│   └── sequential_thinking_service.py  # Sequential thinking operations
├── tools/                              # MCP tools
│   ├── arxiv_tools.py                 # ArXiv MCP tools
│   └── sequential_thinking_tools.py   # Sequential thinking MCP tools
├── utils/                              # Shared components
│   └── __init__.py                    # Base classes & models
├── README.md                           # Documentation
├── QUICKSTART.md                      # Quick start guide
├── test_server.py                     # Test suite
├── Dockerfile                         # Docker configuration
├── docker-compose.yml                 # Docker Compose setup
├── setup-docker.sh                    # Docker setup script
├── run_mcp_docker.sh                  # Docker wrapper for Claude Desktop
├── claude_desktop_config_docker.json  # Docker config template
├── requirements.txt                   # Dependencies
└── .gitignore                         # Git ignore rules
```

## 🐳 **Why Docker?**

Docker provides several advantages for MCP servers:

### **✅ Benefits**
- **No Python Environment Setup**: Eliminates virtual environment complexity
- **Consistent Environment**: Same behavior across all systems
- **Easy Installation**: Just `docker build` and you're ready
- **Isolation**: No conflicts with system Python packages
- **Portability**: Works on any system with Docker
- **Easy Updates**: Rebuild image to update dependencies

## 🚀 **Features**

- **8 ArXiv Tools**: Search, details, recent papers, author papers, trending categories, advanced search, version support, phrase search
- **3 Sequential Thinking Tools**: Dynamic problem-solving, thought revision, branching analysis
- **Advanced Query Support**: Boolean operators (AND, OR, ANDNOT), field-specific searches, phrase matching
- **Enhanced Metadata**: Journal references, DOI links, author comments, affiliations, primary categories
- **Version Support**: Access specific versions of papers
- **Docker-Based**: Containerized deployment for easy setup
- **Modular Design**: Easy to add new services and tools
- **Scalable Architecture**: Clean separation of concerns
- **Local Operation**: Runs entirely on your local machine
- **Claude Desktop Integration**: Seamlessly integrates with Claude Desktop

## 📋 **Available Tools**

### ArXiv Tools
1. **`search_arxiv`** - Search papers by query with sorting options
2. **`get_paper_details`** - Get detailed information about specific papers
3. **`get_recent_papers`** - Get recent papers from specific categories
4. **`get_papers_by_author`** - Get papers by specific authors
5. **`get_trending_categories`** - Get trending categories with paper counts
6. **`advanced_search`** - Multi-field search with Boolean operators and date ranges
7. **`get_paper_by_version`** - Get specific versions of papers
8. **`search_by_phrase`** - Search for exact phrases in titles, abstracts, or authors

### Sequential Thinking Tools
1. **`sequential_thinking`** - Dynamic problem-solving through structured thoughts
2. **`get_thought_summary`** - Get summary of current thinking session
3. **`clear_thought_history`** - Clear thought history and branches

## 🛠️ **Installation**

### Prerequisites
- Git (to clone the repository)
- Docker (for containerized installation)

## 🐳 **Docker Installation**

### Quick Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/brandont/arxiv-mcp-server.git
   cd arxiv-mcp-server
   ```

2. **Run the Docker setup script**:
   ```bash
   chmod +x setup-docker.sh
   ./setup-docker.sh
   ```

3. **Test the Docker container**:
   ```bash
   docker run --rm multi-service-mcp-server python test_server.py --test
   ```

### Manual Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/brandont/arxiv-mcp-server.git
   cd arxiv-mcp-server
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t multi-service-mcp-server .
   ```

3. **Test the installation**:
   ```bash
   docker run --rm multi-service-mcp-server python test_server.py --test
   ```

## 🔧 **Claude Desktop Integration**

1. **Locate your Claude Desktop configuration file**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the Docker MCP server configuration**:
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
   
   **Important**: Replace `/path/to/your/multi-service-mcp-server` with the actual path where you cloned this repository

3. **Alternative: Use the Docker config file**:
   ```bash
   # Copy the Docker config and update the path
   cp claude_desktop_config_docker.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
   # Then edit the file to add the correct path to run_mcp_docker.sh
   ```

4. **Restart Claude Desktop** to load the new MCP server.

### Verification
Once configured, you can test the tools in Claude Desktop:
- "Search ArXiv for papers on machine learning"
- "Get details for paper 2301.00001"
- "Show me recent papers in cs.AI"
- "Get papers by author Geoffrey Hinton"
- "What are the trending categories this month?"
- "Advanced search: papers by Yann LeCun in cs.AI category from 2023"
- "Get version 2 of paper 2301.00001"
- "Search for exact phrase 'neural networks' in titles"

## 🔍 **Advanced Search Features**

Based on the [ArXiv API documentation](https://info.arxiv.org/help/api/user-manual.html), this server supports:

### **Boolean Operators**
- `AND` - Combine search terms
- `OR` - Find papers matching any term
- `ANDNOT` - Exclude certain terms

### **Field-Specific Searches**
- `au:` - Author name (e.g., `au:LeCun`)
- `ti:` - Title keywords (e.g., `ti:neural networks`)
- `abs:` - Abstract keywords (e.g., `abs:machine learning`)
- `cat:` - ArXiv category (e.g., `cat:cs.AI`)

### **Phrase Matching**
- Use double quotes for exact phrases: `"deep learning"`

### **Date Ranges**
- Format: `YYYYMMDD` (e.g., `20230101`)
- Range: `submittedDate:[20230101 TO 20231231]`

### **Example Advanced Queries**
```
# Papers by LeCun about neural networks in AI category
au:LeCun AND ti:neural AND cat:cs.AI

# Recent papers excluding certain categories
submittedDate:[20240101 TO *] ANDNOT cat:cs.CV

# Exact phrase in abstract
abs:"transformer architecture"
```

## 🔧 **Adding New Tools**

The modular architecture makes adding new tools incredibly easy:

### Step 1: Add Service Method
```python
# services/arxiv_service.py
def get_papers_by_keyword(self, keyword: str) -> List[PaperInfo]:
    """Get papers containing a specific keyword."""
    # Implementation here
    pass
```

### Step 2: Add Tool
```python
# tools/arxiv_tools.py
@self.mcp.tool()
async def get_papers_by_keyword(keyword: str) -> str:
    """
    Get papers containing a specific keyword.
    
    Args:
        keyword: Keyword to search for
    
    Returns:
        JSON string containing matching papers
    """
    try:
        results = self.service.get_papers_by_keyword(keyword)
        return json.dumps([paper.model_dump() for paper in results], indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
```

### Step 3: Restart Server
That's it! The tool is automatically registered and available in Claude Desktop.

## 🏗️ **Adding New Services**

To add a completely new service (e.g., Weather, News):

### Step 1: Create Service
```python
# services/weather_service.py
from utils import BaseService

class WeatherService(BaseService):
    def get_name(self) -> str:
        return "Weather"
    
    def get_weather(self, city: str) -> dict:
        # Weather API logic
        pass
```

### Step 2: Create Tool Provider
```python
# tools/weather_tools.py
from utils import BaseToolProvider

class WeatherToolProvider(BaseToolProvider):
    def _register_tools(self):
        @self.mcp.tool()
        async def get_weather(city: str) -> str:
            """Get weather for a city."""
            result = self.service.get_weather(city)
            return json.dumps(result, indent=2)
```

### Step 3: Register in Main Server
```python
# server.py
from mcp.server.fastmcp import FastMCP
from services.arxiv_service import ArXivService
from services.weather_service import WeatherService
from tools.arxiv_tools import ArXivToolProvider
from tools.weather_tools import WeatherToolProvider

# Create the MCP server
mcp = FastMCP("Multi-Service MCP Server")

# Initialize services and tools
arxiv_service = ArXivService()
arxiv_tools = ArXivToolProvider(mcp, arxiv_service)

weather_service = WeatherService()
weather_tools = WeatherToolProvider(mcp, weather_service)
```

## 🧪 **Testing**

Run the test suite to verify everything works:
```bash
docker run --rm multi-service-mcp-server python test_server.py --test
```

## 🚨 **Troubleshooting**

### Common Issues
1. **Claude Desktop not recognizing the server**: 
   - Check that the path in the configuration file points to `run_mcp_docker.sh`
   - Ensure Claude Desktop is restarted after configuration changes
   - Verify the wrapper script is executable: `chmod +x run_mcp_docker.sh`
2. **ArXiv API errors**: 
   - Check your internet connection and ArXiv accessibility
   - Some queries may fail due to ArXiv API limits
3. **Docker issues**:
   - Make sure Docker is installed and running: `docker --version`
   - For Docker daemon issues, restart Docker Desktop
   - Ensure the Docker image is built: `docker build -t multi-service-mcp-server .`
4. **Permission errors on setup script**:
   - Run `chmod +x setup-docker.sh` to make the script executable

### Getting Help
- Check logs for detailed error information
- Run the test suite to verify functionality: `docker run --rm multi-service-mcp-server python test_server.py --test`
- Ensure Docker is properly installed and running
- Verify the Docker image is built correctly

## 📊 **Technical Details**

- **Framework**: Built using the official MCP Python SDK
- **Architecture**: Modular service-based design
- **Deployment**: Docker containerized
- **ArXiv Access**: Uses the `arxiv` Python library
- **Transport**: STDIO transport for Claude Desktop integration
- **Tool Definition**: Auto-generated from Python type hints and docstrings

## 📄 **License**

This project is open source and available under the MIT License.
