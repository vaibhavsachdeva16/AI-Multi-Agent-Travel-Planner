from prompts.itinerary_prompt import itinerary_prompt
from tools.llm import get_llm
from langchain_core.output_parsers import StrOutputParser
from utils.state import TravelState


llm = get_llm()

itinerary_chain = (
    itinerary_prompt
    | llm
    | StrOutputParser()
)


def itinerary_agent(state: TravelState) -> dict:
    """
    Generate the complete travel itinerary.
    """

    itinerary = itinerary_chain.invoke(
        {
            "destination": state["destination"],
            "duration": state["duration"],
            "preferences": state["preferences"],
            "budget_plan": state["budget_plan"],
            "weather": state["weather"],
            "hotels": state["hotels"],
            "attractions": state["attractions"],
            "transport": state["transport"],
            "travelers": state["travelers"],
        }
    )

    return {
        "itinerary": itinerary
    }
