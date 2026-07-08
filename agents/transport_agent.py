from prompts.transport_prompt import transport_prompt
from tools.llm import get_structured_llm
from tools.search import search
from utils.models import TransportRecommendations
from utils.state import TravelState


structured_llm = get_structured_llm(TransportRecommendations)

transport_chain = transport_prompt | structured_llm


def transport_agent(state: TravelState) -> dict:
    """
    Recommend transportation options using live Tavily search.
    """

    transport_budget = state["budget_plan"]["transport"]

    search_results = search(
        query=(
            f"Best transportation options from "
            f"{state['source']} to {state['destination']} "
            f"including flight, train and bus fares "
            f"for {state['travelers']} people"
        ),
        max_results=5,
    )

    transport = transport_chain.invoke(
        {
            "search_results": str(search_results),
            "source": state["source"],
            "destination": state["destination"],
            "transport_budget": transport_budget,
            "travelers": state["travelers"],
        }
    )

    return {
        "transport": transport.model_dump()["transport"]
    }
