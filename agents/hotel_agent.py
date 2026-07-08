from prompts.hotel_prompt import hotel_prompt
from tools.llm import get_structured_llm
from tools.search import search
from utils.models import HotelRecommendations
from utils.state import TravelState


structured_llm = get_structured_llm(HotelRecommendations)

hotel_chain = hotel_prompt | structured_llm


def hotel_agent(state: TravelState) -> dict:
    """
    Generate hotel recommendations using live Tavily search results.
    """

    hotel_budget = state["budget_plan"]["hotel"]
    duration = state["duration"]

    nights = max(duration - 1, 1)

    per_night_budget = hotel_budget // nights

    search_results = search(
        query=(
            f"Best hotels in {state['destination']} "
            f"under ₹{per_night_budget} per night "
            f"for a {duration}-day trip "
            f"for {state['travelers']} people "
            f"with {state['preferences']} preferences"
        ),
        max_results=5,
    )

    hotels = hotel_chain.invoke(
        {
            "search_results": str(search_results),
            "hotel_budget": hotel_budget,
            "per_night_budget": per_night_budget,
            "duration": duration,
            "travelers": state["travelers"],
        }
    )

    return {
        "hotels": hotels.model_dump()["hotels"]
    }
