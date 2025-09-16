"""
ArXiv tool provider for MCP server.
"""

import json
from utils import BaseToolProvider


class ArXivToolProvider(BaseToolProvider):
    """Tool provider for ArXiv operations."""
    
    def _register_tools(self):
        """Register ArXiv tools with the MCP server."""
        
        @self.mcp.tool()
        async def search_arxiv(
            query: str,
            max_results: int = 10,
            sort_by: str = "relevance",
            sort_order: str = "desc"
        ) -> str:
            """
            Search ArXiv for papers matching the query.
            
            Args:
                query: Search query (can include authors, keywords, categories)
                max_results: Maximum number of results to return (default: 10, max: 50)
                sort_by: Sort criteria - 'relevance', 'submittedDate', 'lastUpdatedDate'
                sort_order: Sort order - 'asc' or 'desc'
            
            Returns:
                JSON string containing search results
            """
            try:
                results = self.service.search_papers(query, max_results, sort_by, sort_order)
                return json.dumps({
                    "query": query,
                    "total_results": len(results),
                    "papers": [paper.model_dump() for paper in results]
                }, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Search failed: {str(e)}",
                    "query": query,
                    "papers": []
                })
        
        @self.mcp.tool()
        async def get_paper_details(arxiv_id: str) -> str:
            """
            Get detailed information about a specific ArXiv paper.
            
            Args:
                arxiv_id: ArXiv paper ID (e.g., '2301.00001' or '2301.00001v1')
            
            Returns:
                JSON string containing detailed paper information
            """
            try:
                paper = self.service.get_paper_by_id(arxiv_id)
                if not paper:
                    return json.dumps({
                        "error": f"Paper {arxiv_id} not found",
                        "arxiv_id": arxiv_id
                    })
                
                return json.dumps(paper.model_dump(), indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to fetch paper details: {str(e)}",
                    "arxiv_id": arxiv_id
                })
        
        @self.mcp.tool()
        async def get_recent_papers(
            category: str = "cs.AI",
            days_back: int = 7,
            max_results: int = 20
        ) -> str:
            """
            Get recent papers from a specific ArXiv category.
            
            Args:
                category: ArXiv category (e.g., 'cs.AI', 'cs.LG', 'math.CO')
                days_back: Number of days to look back (default: 7)
                max_results: Maximum number of results (default: 20, max: 50)
            
            Returns:
                JSON string containing recent papers
            """
            try:
                results = self.service.get_recent_papers(category, days_back, max_results)
                return json.dumps({
                    "category": category,
                    "days_back": days_back,
                    "total_results": len(results),
                    "papers": [paper.model_dump() for paper in results]
                }, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to fetch recent papers: {str(e)}",
                    "category": category,
                    "papers": []
                })
        
        @self.mcp.tool()
        async def get_papers_by_author(
            author_name: str,
            max_results: int = 10
        ) -> str:
            """
            Get papers by a specific author.
            
            Args:
                author_name: Name of the author to search for
                max_results: Maximum number of results to return (default: 10, max: 50)
            
            Returns:
                JSON string containing papers by the author
            """
            try:
                results = self.service.get_papers_by_author(author_name, max_results)
                return json.dumps({
                    "author": author_name,
                    "total_results": len(results),
                    "papers": [paper.model_dump() for paper in results]
                }, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to fetch papers by author: {str(e)}",
                    "author": author_name,
                    "papers": []
                })
        
        @self.mcp.tool()
        async def get_trending_categories(
            days_back: int = 30,
            min_papers: int = 5
        ) -> str:
            """
            Get trending categories based on recent paper counts.
            
            Args:
                days_back: Number of days to look back (default: 30)
                min_papers: Minimum number of papers required for a category to be trending (default: 5)
            
            Returns:
                JSON string containing trending categories with paper counts
            """
            try:
                trending = self.service.get_trending_categories(days_back, min_papers)
                return json.dumps({
                    "days_back": days_back,
                    "min_papers": min_papers,
                    "trending_categories": trending
                }, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to fetch trending categories: {str(e)}",
                    "trending_categories": {}
                })
        
        @self.mcp.tool()
        async def advanced_search(
            query: str = "",
            author: str = "",
            title: str = "",
            abstract: str = "",
            category: str = "",
            exclude_category: str = "",
            start_date: str = "",
            end_date: str = "",
            max_results: int = 10,
            sort_by: str = "relevance",
            sort_order: str = "desc"
        ) -> str:
            """
            Advanced search with multiple field support using ArXiv API query syntax.
            
            Args:
                query: General search query
                author: Author name (uses au: prefix)
                title: Title keywords (uses ti: prefix)
                abstract: Abstract keywords (uses abs: prefix)
                category: ArXiv category (uses cat: prefix)
                exclude_category: Category to exclude (uses ANDNOT cat: prefix)
                start_date: Start date in YYYYMMDD format
                end_date: End date in YYYYMMDD format
                max_results: Maximum number of results (default: 10, max: 200)
                sort_by: Sort criteria - 'relevance', 'submittedDate', 'lastUpdatedDate'
                sort_order: Sort order - 'asc' or 'desc'
            
            Returns:
                JSON string containing advanced search results
            """
            try:
                results = self.service.advanced_search(
                    query=query,
                    author=author,
                    title=title,
                    abstract=abstract,
                    category=category,
                    exclude_category=exclude_category,
                    start_date=start_date,
                    end_date=end_date,
                    max_results=max_results,
                    sort_by=sort_by,
                    sort_order=sort_order
                )
                return json.dumps({
                    "query_params": {
                        "query": query,
                        "author": author,
                        "title": title,
                        "abstract": abstract,
                        "category": category,
                        "exclude_category": exclude_category,
                        "start_date": start_date,
                        "end_date": end_date
                    },
                    "total_results": len(results),
                    "papers": [paper.model_dump() for paper in results]
                }, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Advanced search failed: {str(e)}",
                    "query_params": {
                        "query": query,
                        "author": author,
                        "title": title,
                        "abstract": abstract,
                        "category": category,
                        "exclude_category": exclude_category,
                        "start_date": start_date,
                        "end_date": end_date
                    },
                    "papers": []
                })
        
        @self.mcp.tool()
        async def get_paper_by_version(arxiv_id: str, version: int) -> str:
            """
            Get a specific version of a paper.
            
            Args:
                arxiv_id: ArXiv paper ID (without version)
                version: Version number (e.g., 1, 2, 3)
            
            Returns:
                JSON string containing paper information for the specific version
            """
            try:
                paper = self.service.get_paper_by_version(arxiv_id, version)
                if not paper:
                    return json.dumps({
                        "error": f"Paper {arxiv_id}v{version} not found",
                        "arxiv_id": arxiv_id,
                        "version": version
                    })
                
                return json.dumps(paper.model_dump(), indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to fetch paper version: {str(e)}",
                    "arxiv_id": arxiv_id,
                    "version": version
                })
        
        @self.mcp.tool()
        async def search_by_phrase(
            phrase: str,
            field: str = "all",
            max_results: int = 10
        ) -> str:
            """
            Search for exact phrases using double quotes.
            
            Args:
                phrase: Exact phrase to search for
                field: Field to search in ('all', 'title', 'abstract', 'author')
                max_results: Maximum number of results (default: 10, max: 50)
            
            Returns:
                JSON string containing phrase search results
            """
            try:
                results = self.service.search_by_phrase(phrase, field, max_results)
                return json.dumps({
                    "phrase": phrase,
                    "field": field,
                    "total_results": len(results),
                    "papers": [paper.model_dump() for paper in results]
                }, indent=2)
            except Exception as e:
                return json.dumps({
                    "error": f"Phrase search failed: {str(e)}",
                    "phrase": phrase,
                    "field": field,
                    "papers": []
                })
