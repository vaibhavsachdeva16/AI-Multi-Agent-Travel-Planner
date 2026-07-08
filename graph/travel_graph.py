from langgraph.graph import START, END, StateGraph

from agents.itinerary_agent import itinerary_agent
from agents.transport_agent import transport_agent
from agents.attractions_agent import attractions_agent
from agents.budget_agent import budget_agent
from agents.destination_agent import destination_agent
from agents.hotel_agent import hotel_agent
from agents.weather_agent import weather_agent
from utils.state import TravelState


def build_graph():
    workflow = StateGraph(TravelState)

    workflow.add_node("destination", destination_agent)
    workflow.add_node("budget", budget_agent)
    workflow.add_node("hotel", hotel_agent)
    workflow.add_node("weather", weather_agent)
    workflow.add_node("attractions", attractions_agent)
    workflow.add_node("transport", transport_agent)
    workflow.add_node("itinerary", itinerary_agent)

    workflow.add_edge(START, "destination")
    workflow.add_edge("destination", "budget")
    workflow.add_edge("budget", "hotel")
    workflow.add_edge("hotel", "weather")
    workflow.add_edge("weather", "attractions")
    workflow.add_edge("attractions", "transport")
    workflow.add_edge("transport", "itinerary")
    workflow.add_edge("itinerary", END)

    return workflow.compile()
