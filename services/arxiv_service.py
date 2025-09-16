"""
ArXiv service for handling ArXiv API operations.
"""

from typing import List, Optional
from datetime import datetime, timedelta

import arxiv
from utils import BaseService, PaperInfo


class ArXivService(BaseService):
    """Service class for ArXiv operations."""
    
    def get_name(self) -> str:
        return "ArXiv"
    
    def _create_paper_info(self, result) -> PaperInfo:
        """Create a PaperInfo object from an ArXiv result."""
        # Extract version from entry_id if present
        arxiv_id = result.entry_id.split('/')[-1]
        version = None
        if 'v' in arxiv_id:
            version = arxiv_id.split('v')[-1]
            arxiv_id = arxiv_id.split('v')[0]
        
        # Create ArXiv abstract URL
        arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
        if version:
            arxiv_url = f"https://arxiv.org/abs/{arxiv_id}v{version}"
        
        return PaperInfo(
            arxiv_id=arxiv_id,
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            published=result.published.isoformat(),
            updated=result.updated.isoformat(),
            categories=result.categories,
            pdf_url=result.pdf_url,
            arxiv_url=arxiv_url,
            summary=f"{result.title} by {', '.join(author.name for author in result.authors[:3])}{'...' if len(result.authors) > 3 else ''}",
            primary_category=getattr(result, 'primary_category', None),
            journal_ref=getattr(result, 'journal_ref', None),
            doi=getattr(result, 'doi', None),
            comment=getattr(result, 'comment', None),
            version=version
        )
    
    def search_papers(self, query: str, max_results: int = 10, sort_by: str = "relevance", sort_order: str = "desc") -> List[PaperInfo]:
        """Search ArXiv for papers matching the query."""
        max_results = min(max_results, 50)
        
        sort_criteria = {
            "relevance": arxiv.SortCriterion.Relevance,
            "submittedDate": arxiv.SortCriterion.SubmittedDate,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate
        }.get(sort_by, arxiv.SortCriterion.Relevance)
        
        sort_order_enum = arxiv.SortOrder.Descending if sort_order == "desc" else arxiv.SortOrder.Ascending
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criteria,
            sort_order=sort_order_enum
        )
        
        results = []
        for result in search.results():
            paper_info = self._create_paper_info(result)
            results.append(paper_info)
        
        return results
    
    def get_paper_by_id(self, arxiv_id: str) -> Optional[PaperInfo]:
        """Get a specific paper by ArXiv ID."""
        search = arxiv.Search(id_list=[arxiv_id])
        result = next(search.results(), None)
        
        if not result:
            return None
        
        return self._create_paper_info(result)
    
    def get_recent_papers(self, category: str = "cs.AI", days_back: int = 7, max_results: int = 20) -> List[PaperInfo]:
        """Get recent papers from a specific ArXiv category."""
        max_results = min(max_results, 50)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        date_query = f"cat:{category} AND submittedDate:[{start_date.strftime('%Y%m%d')} TO {end_date.strftime('%Y%m%d')}]"
        
        search = arxiv.Search(
            query=date_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        results = []
        for result in search.results():
            paper_info = self._create_paper_info(result)
            results.append(paper_info)
        
        return results
    
    def get_papers_by_author(self, author_name: str, max_results: int = 10) -> List[PaperInfo]:
        """Get papers by a specific author."""
        max_results = min(max_results, 50)
        
        query = f"au:{author_name}"
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        results = []
        for result in search.results():
            paper_info = self._create_paper_info(result)
            results.append(paper_info)
        
        return results
    
    def get_trending_categories(self, days_back: int = 30, min_papers: int = 5) -> dict:
        """Get trending categories based on recent paper counts."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        category_counts = {}
        
        # Use a smaller, more reliable query approach
        # Query recent papers with a reasonable limit
        date_query = f"submittedDate:[{start_date.strftime('%Y%m%d')} TO {end_date.strftime('%Y%m%d')}]"
        
        try:
            search = arxiv.Search(
                query=date_query,
                max_results=500,  # Reasonable limit that should work
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            # Process results
            for result in search.results():
                for category in result.categories:
                    category_counts[category] = category_counts.get(category, 0) + 1
                    
        except Exception as e:
            # If the main query fails, try with a smaller date range
            print(f"Main query failed: {e}, trying smaller range...")
            
            # Try with last 7 days only
            recent_start = end_date - timedelta(days=7)
            recent_query = f"submittedDate:[{recent_start.strftime('%Y%m%d')} TO {end_date.strftime('%Y%m%d')}]"
            
            try:
                search = arxiv.Search(
                    query=recent_query,
                    max_results=200,
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )
                
                for result in search.results():
                    for category in result.categories:
                        category_counts[category] = category_counts.get(category, 0) + 1
                        
            except Exception as e2:
                print(f"Fallback query also failed: {e2}")
                # Return empty dict if both queries fail
                return {}
        
        trending = {cat: count for cat, count in category_counts.items() if count >= min_papers}
        return dict(sorted(trending.items(), key=lambda x: x[1], reverse=True))
    
    def advanced_search(self, 
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
                       sort_order: str = "desc") -> List[PaperInfo]:
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
            max_results: Maximum number of results
            sort_by: Sort criteria
            sort_order: Sort order
        """
        max_results = min(max_results, 200)  # Increased limit for advanced search
        
        # Build query using ArXiv API syntax
        query_parts = []
        
        if query:
            query_parts.append(query)
        if author:
            query_parts.append(f"au:{author}")
        if title:
            query_parts.append(f"ti:{title}")
        if abstract:
            query_parts.append(f"abs:{abstract}")
        if category:
            query_parts.append(f"cat:{category}")
        if exclude_category:
            query_parts.append(f"ANDNOT cat:{exclude_category}")
        
        # Add date range if provided
        if start_date and end_date:
            query_parts.append(f"submittedDate:[{start_date} TO {end_date}]")
        elif start_date:
            query_parts.append(f"submittedDate:[{start_date} TO *]")
        elif end_date:
            query_parts.append(f"submittedDate:[* TO {end_date}]")
        
        # Combine query parts
        final_query = " AND ".join(query_parts) if query_parts else "*"
        
        sort_criteria = {
            "relevance": arxiv.SortCriterion.Relevance,
            "submittedDate": arxiv.SortCriterion.SubmittedDate,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate
        }.get(sort_by, arxiv.SortCriterion.Relevance)
        
        sort_order_enum = arxiv.SortOrder.Descending if sort_order == "desc" else arxiv.SortOrder.Ascending
        
        search = arxiv.Search(
            query=final_query,
            max_results=max_results,
            sort_by=sort_criteria,
            sort_order=sort_order_enum
        )
        
        results = []
        for result in search.results():
            paper_info = self._create_paper_info(result)
            results.append(paper_info)
        
        return results
    
    def get_paper_by_version(self, arxiv_id: str, version: int) -> Optional[PaperInfo]:
        """Get a specific version of a paper."""
        versioned_id = f"{arxiv_id}v{version}"
        search = arxiv.Search(id_list=[versioned_id])
        result = next(search.results(), None)
        
        if not result:
            return None
        
        return self._create_paper_info(result)
    
    def search_by_phrase(self, phrase: str, field: str = "all", max_results: int = 10) -> List[PaperInfo]:
        """
        Search for exact phrases using double quotes.
        
        Args:
            phrase: Exact phrase to search for
            field: Field to search in ('all', 'title', 'abstract', 'author')
            max_results: Maximum number of results
        """
        max_results = min(max_results, 50)
        
        # Add quotes around phrase for exact matching
        quoted_phrase = f'"{phrase}"'
        
        if field == "title":
            query = f"ti:{quoted_phrase}"
        elif field == "abstract":
            query = f"abs:{quoted_phrase}"
        elif field == "author":
            query = f"au:{quoted_phrase}"
        else:
            query = quoted_phrase
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )
        
        results = []
        for result in search.results():
            paper_info = self._create_paper_info(result)
            results.append(paper_info)
        
        return results
