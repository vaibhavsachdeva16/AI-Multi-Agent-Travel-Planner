from langchain_tavily import TavilySearch

from utils.config import TAVILY_API_KEY, validate_config

validate_config()


def search(query: str, max_results: int = 5):
    """
    Search the web using Tavily.
    """

    search_tool = TavilySearch(
        max_results=max_results,
        tavily_api_key=TAVILY_API_KEY,
    )

    return search_tool.invoke(query)
