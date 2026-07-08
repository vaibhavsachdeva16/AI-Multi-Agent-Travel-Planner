from utils.state import TravelState


def budget_agent(state: TravelState) -> dict:
    """
    Calculate budget allocation using deterministic Python logic.
    """

    total_budget = state["budget"]

    hotel = int(total_budget * 0.40)
    food = int(total_budget * 0.25)
    transport = int(total_budget * 0.15)

    # Remaining budget goes to activities
    activities = total_budget - hotel - food - transport

    return {
        "budget_plan": {
            "hotel": hotel,
            "food": food,
            "transport": transport,
            "activities": activities,
            "total": total_budget,
        }
    }
