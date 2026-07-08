from typing import List
from pydantic import BaseModel, Field


class Hotel(BaseModel):
    """
    Hotel recommendation.
    """

    name: str = Field(description="Hotel name")
    price_per_night: int = Field(description="Estimated price per night in INR")
    rating: float = Field(description="Hotel rating out of 5")
    location: str = Field(description="Area where the hotel is located")


class HotelRecommendations(BaseModel):
    """
    List of hotel recommendations.
    """

    hotels: List[Hotel]


class WeatherInfo(BaseModel):
    """
    Current weather information for the destination.
    """

    condition: str = Field(description="Current weather condition")
    temperature: int = Field(description="Temperature in Celsius")
    travel_advice: str = Field(description="Travel advice based on the weather")


class Attraction(BaseModel):
    name: str = Field(description="Tourist attraction name")
    description: str = Field(description="Short description")


class AttractionRecommendations(BaseModel):
    """
    List of tourist attractions.
    """

    attractions: List[Attraction]


class TransportOption(BaseModel):
    """
    Transport option between source and destination.
    """

    mode: str = Field(description="Mode of transport")
    estimated_cost: int = Field(description="Estimated one-way cost in INR")
    estimated_time: str = Field(description="Estimated travel time")
    description: str = Field(description="Short description")


class TransportRecommendations(BaseModel):
    """
    List of transport options.
    """

    transport: List[TransportOption]
