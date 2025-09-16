#!/usr/bin/env python3
"""
Test script for ArXiv MCP Server

This script tests the MCP server functionality without requiring Claude Desktop.
"""

import sys
from services.arxiv_service import ArXivService


def test_search():
    """Test the search_papers service method."""
    print("Testing search_papers service method...")
    
    service = ArXivService()
    
    # Test basic search
    results = service.search_papers(
        query="machine learning",
        max_results=3,
        sort_by="relevance",
        sort_order="desc"
    )
    
    print(f"✓ Search test passed - found {len(results)} papers")
    
    if results:
        print(f"  First paper: {results[0].title[:50]}...")
    
    return True


def test_paper_details():
    """Test the get_paper_by_id service method."""
    print("Testing get_paper_by_id service method...")
    
    service = ArXivService()
    
    # Test with a known paper ID
    result = service.get_paper_by_id("2301.00001")
    
    if result:
        print(f"✓ Paper details test passed - {result.title[:50]}...")
        return True
    else:
        print("⚠ Paper details test - Paper not found")
        return False


def test_recent_papers():
    """Test the get_recent_papers service method."""
    print("Testing get_recent_papers service method...")
    
    service = ArXivService()
    
    results = service.get_recent_papers(
        category="cs.AI",
        days_back=30,
        max_results=3
    )
    
    print(f"✓ Recent papers test passed - found {len(results)} papers")
    
    if results:
        print(f"  First paper: {results[0].title[:50]}...")
    
    return True


def test_papers_by_author():
    """Test the get_papers_by_author service method."""
    print("Testing get_papers_by_author service method...")
    
    service = ArXivService()
    
    results = service.get_papers_by_author(
        author_name="Geoffrey Hinton",
        max_results=3
    )
    
    print(f"✓ Papers by author test passed - found {len(results)} papers")
    
    if results:
        print(f"  First paper: {results[0].title[:50]}...")
    
    return True


def test_trending_categories():
    """Test the get_trending_categories service method."""
    print("Testing get_trending_categories service method...")
    
    service = ArXivService()
    
    trending = service.get_trending_categories(
        days_back=30,
        min_papers=3
    )
    
    print(f"✓ Trending categories test passed - found {len(trending)} categories")
    
    if trending:
        top_category = list(trending.keys())[0]
        print(f"  Top category: {top_category} ({trending[top_category]} papers)")
    
    return True


def run_tests():
    """Run all tests."""
    print("🧪 Running ArXiv MCP Server Tests\n")
    
    tests = [
        ("Search Papers", test_search),
        ("Paper Details", test_paper_details),
        ("Recent Papers", test_recent_papers),
        ("Papers by Author", test_papers_by_author),
        ("Trending Categories", test_trending_categories),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            if success:
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} test failed: {str(e)}")
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The MCP server is ready to use.")
        return 0
    else:
        print("⚠ Some tests failed. Check the logs for details.")
        return 1


if __name__ == "__main__":
    # Check if --test flag is provided
    if "--test" in sys.argv:
        exit_code = run_tests()
        sys.exit(exit_code)
    else:
        print("ArXiv MCP Server Test Script")
        print("Run with --test flag to execute tests")
        print("Example: python3 test_server.py --test")
