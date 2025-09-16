"""
Shared data models and utilities for the MCP server.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PaperInfo(BaseModel):
    """Model for paper information."""
    arxiv_id: str = Field(..., description="ArXiv paper ID")
    title: str = Field(..., description="Paper title")
    authors: List[str] = Field(..., description="List of authors")
    abstract: str = Field(..., description="Paper abstract")
    published: str = Field(..., description="Publication date")
    updated: str = Field(..., description="Last updated date")
    categories: List[str] = Field(..., description="ArXiv categories")
    pdf_url: str = Field(..., description="URL to PDF")
    arxiv_url: str = Field(..., description="URL to ArXiv abstract page")
    summary: str = Field(..., description="Brief summary")
    # Additional fields from ArXiv API
    primary_category: Optional[str] = Field(None, description="Primary ArXiv category")
    journal_ref: Optional[str] = Field(None, description="Journal reference if published")
    doi: Optional[str] = Field(None, description="DOI link if available")
    comment: Optional[str] = Field(None, description="Author comment")
    version: Optional[str] = Field(None, description="Paper version")


class ThoughtData(BaseModel):
    """Model for sequential thinking data."""
    thought: str = Field(..., description="The current thinking step")
    thought_number: int = Field(..., description="Current thought number in sequence", ge=1)
    total_thoughts: int = Field(..., description="Estimated total thoughts needed", ge=1)
    next_thought_needed: bool = Field(..., description="Whether another thought step is needed")
    is_revision: Optional[bool] = Field(None, description="Whether this revises previous thinking")
    revises_thought: Optional[int] = Field(None, description="Which thought is being reconsidered", ge=1)
    branch_from_thought: Optional[int] = Field(None, description="Branching point thought number", ge=1)
    branch_id: Optional[str] = Field(None, description="Branch identifier")
    needs_more_thoughts: Optional[bool] = Field(None, description="If more thoughts are needed")


class ThoughtResponse(BaseModel):
    """Model for thought processing response."""
    thought_number: int = Field(..., description="Current thought number")
    total_thoughts: int = Field(..., description="Total thoughts estimate")
    next_thought_needed: bool = Field(..., description="Whether more thoughts needed")
    branches: List[str] = Field(..., description="List of branch IDs")
    thought_history_length: int = Field(..., description="Length of thought history")
    error: Optional[str] = Field(None, description="Error message if any")
    status: Optional[str] = Field(None, description="Status of processing")


class BaseService:
    """Base class for all services."""
    
    def get_name(self) -> str:
        """Return the service name."""
        raise NotImplementedError


class BaseToolProvider:
    """Base class for tool providers."""
    
    def __init__(self, mcp, service: BaseService):
        self.mcp = mcp
        self.service = service
        self._register_tools()
    
    def _register_tools(self):
        """Register tools with the MCP server."""
        raise NotImplementedError
