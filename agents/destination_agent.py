from langchain_core.output_parsers import StrOutputParser

from prompts.destination_prompt import destination_prompt
from tools.llm import get_llm
from utils.state import TravelState


llm = get_llm()

parser = StrOutputParser()

destination_chain = destination_prompt | llm | parser


def destination_agent(state: TravelState) -> dict:
    """
    Extract the travel destination from the user's query.
    """

    destination = destination_chain.invoke(
        {
            "user_query": state["user_query"]
        }
    )

    return {
        "destination": destination.strip()
    }
