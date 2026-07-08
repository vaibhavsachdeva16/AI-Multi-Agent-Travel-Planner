from typing import Any, Dict, List, TypedDict


class TravelState(TypedDict):
    """
    Shared state used across all LangGraph agents.
    """

    # User Input
    user_query: str
    source: str
    destination: str
    duration: int
    budget: int
    travelers: int
    preferences: str

    # Agent Outputs
    budget_plan: Dict[str, int]
    weather: Dict[str, Any]
    hotels: List[str]
    attractions: List[Dict[str, Any]]
    transport: List[Dict[str, Any]]
    itinerary: str

    # Final Output
    final_response: str
