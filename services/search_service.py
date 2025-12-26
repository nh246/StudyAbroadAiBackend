# Search Service - Tavily web search integration

from typing import List, Dict
from core.config import settings


def search_web(query: str, max_results: int = 5) -> Dict:
    """
    Search the web using Tavily API
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary with search results and sources
    """
    try:
        from tavily import TavilyClient
        
        # Initialize Tavily client
        client = TavilyClient(api_key=settings.tavily_api_key)
        
        # Perform search
        response = client.search(
            query=query,
            search_depth="advanced",  # or "basic" for faster results
            max_results=max_results,
            include_answer=True,  # Get a summarized answer
            include_raw_content=False  # Don't need full page content
        )
        
        # Extract relevant information
        results = {
            "answer": response.get("answer", ""),
            "sources": []
        }
        
        # Format sources
        for result in response.get("results", []):
            results["sources"].append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", "")
            })
        
        return results
        
    except ImportError:
        # Fallback if tavily-python not installed
        return {
            "answer": "Tavily search not available. Please install: pip install tavily-python",
            "sources": []
        }
    except Exception as e:
        return {
            "answer": f"Search error: {str(e)}",
            "sources": []
        }


def format_search_results(search_data: Dict) -> str:
    """
    Format search results into a readable string for AI
    
    Args:
        search_data: Dictionary from search_web()
        
    Returns:
        Formatted string with search context
    """
    if not search_data.get("sources"):
        return "No relevant search results found."
    
    formatted = "Web Search Results:\n\n"
    
    if search_data.get("answer"):
        formatted += f"Summary: {search_data['answer']}\n\n"
    
    formatted += "Sources:\n"
    for idx, source in enumerate(search_data["sources"], 1):
        formatted += f"{idx}. {source['title']}\n"
        formatted += f"   {source['snippet'][:200]}...\n"
        formatted += f"   URL: {source['url']}\n\n"
    
    return formatted.strip()
