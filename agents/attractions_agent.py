from prompts.attractions_prompt import attractions_prompt
from tools.llm import get_structured_llm
from tools.search import search
from utils.models import AttractionRecommendations
from utils.state import TravelState


structured_llm = get_structured_llm(AttractionRecommendations)

attractions_chain = attractions_prompt | structured_llm


def attractions_agent(state: TravelState) -> dict:
    """
    Recommend tourist attractions using live Tavily search.
    """

    search_results = search(
        query=(
            f"Top tourist attractions in {state['destination']} "
            f"for {state['preferences']} "
            f"including historical places, sightseeing, local experiences and must visit places"
        ),
        max_results=5,
    )

    attractions = attractions_chain.invoke(
        {
            "search_results": str(search_results),
            "destination": state["destination"],
            "preferences": state["preferences"],
            "weather": state["weather"]["condition"],
        }
    )

    return {
        "attractions": attractions.model_dump()["attractions"]
    }
