from graph.travel_graph import build_graph


def main():

    graph = build_graph()

    result = graph.invoke(
        {
            "user_query": "Plan a 5-day trip to Goa under ₹40,000.",
            "source": "",
            "destination": "",
            "duration": 5,
            "budget": 40000,
            "travelers": 2,
            "preferences": "",
            "weather": "",
            "hotels": [],
            "attractions": [],
            "transport": [],
            "itinerary": "",
            "final_response": "",
        }
    )

    print(result)


if __name__ == "__main__":
    main()