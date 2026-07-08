from prompts.weather_prompt import weather_prompt
from tools.llm import get_structured_llm
from tools.search import search
from utils.models import WeatherInfo
from utils.state import TravelState


structured_llm = get_structured_llm(WeatherInfo)

weather_chain = weather_prompt | structured_llm


def weather_agent(state: TravelState) -> dict:
    """
    Get current weather information using Tavily.
    """

    search_results = search(
        query=f"Current weather in {state['destination']}",
        max_results=3,
    )

    weather = weather_chain.invoke(
        {
            "search_results": str(search_results)
        }
    )

    return {
        "weather": weather.model_dump()
    }
