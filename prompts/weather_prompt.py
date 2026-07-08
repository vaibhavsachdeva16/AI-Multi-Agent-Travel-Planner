from langchain_core.prompts import ChatPromptTemplate


weather_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert travel assistant.

    Based ONLY on the search results below, summarize the current weather.

    Search Results:
    {search_results}

    Rules:
    - Use only the search results.
    - Do not invent weather information.
    - temperature must be an integer in Celsius.
    - travel_advice should be concise (1-2 sentences).
    """
)
