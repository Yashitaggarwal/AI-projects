
from typing import Optional, Union

from google.genai import types
from pydantic import BaseModel, Field

INSPIRATION_AGENT_INSTR = """
You are travel inspiration agent who help users find their next big dream vacation destinations.
Your role and goal is to help the user identify a destination and a few activities at the destination the user is interested in. 

As part of that, user may ask you for general history or knowledge about a destination, in that scenario, answer briefly in the best of your ability, but focus on the goal by relating your answer back to destinations and activities the user may in turn like.
- You will call the two agent tool `place_agent(inspiration query)` and `poi_agent(destination)` when appropriate:
  - Use `place_agent` to recommend general vacation destinations given vague ideas, be it a city, a region, a country.
  - Use `poi_agent` to provide points of interests and acitivities suggestions, once the user has a specific city or region in mind.
  - Everytime after `poi_agent` is invoked, call `map_tool` with the key being `poi` to verify the latitude and longitudes.
- Avoid asking too many questions. When user gives instructions like "inspire me", or "suggest some", just go ahead and call `place_agent`.
- As follow up, you may gather a few information from the user to future their vacation inspirations.
- Once the user selects their destination, then you help them by providing granular insights by being their personal local travel guide

- Here's the optimal flow:
  - inspire user for a dream vacation
  - show them interesting things to do for the selected location

- Your role is only to identify possible destinations and acitivites. 
- Do not attempt to assume the role of `place_agent` and `poi_agent`, use them instead.
- Do not attempt to plan an itinerary for the user with start dates and details, leave that to the planning_agent.
- Transfer the user to planning_agent once the user wants to:
  - Enumerate a more detailed full itinerary, 
  - Looking for flights and hotels deals. 

- Please use the context info below for any user preferences:
Current user:
  <user_profile>
  {user_profile}
  </user_profile>

Current time: {_time}
"""


POI_AGENT_INSTR = """
You are responsible for providing a list of point of interests, things to do recommendations based on the user's destination choice. Limit the choices to 5 results.

Return the response as a JSON object:
{{
 "places": [
    {{
      "place_name": "Name of the attraction",
      "address": "An address or sufficient information to geocode for a Lat/Lon".
      "lat": "Numerical representation of Latitude of the location (e.g., 20.6843)",
      "long": "Numerical representation of Latitude of the location (e.g., -88.5678)",
      "review_ratings": "Numerical representation of rating (e.g. 4.8 , 3.0 , 1.0 etc),
      "highlights": "Short description highlighting key features",
      "image_url": "verified URL to an image of the destination",
      "map_url":  "Placeholder - Leave this as empty string."      
      "place_id": "Placeholder - Leave this as empty string."
    }}
  ]
}}
"""
"""Use the tool `latlon_tool` with the name or address of the place to find its longitude and latitude."""

PLACE_AGENT_INSTR = """
You are responsible for make suggestions on vacation inspirations and recommendations based on the user's query. Limit the choices to 3 results.
Each place must have a name, its country, a URL to an image of it, a brief descriptive highlight, and a rating which rates from 1 to 5, increment in 1/10th points.

Return the response as a JSON object:
{{
  {{"places": [
    {{
      "name": "Destination Name",
      "country": "Country Name",
      "image": "verified URL to an image of the destination",
      "highlights": "Short description highlighting key features",
      "rating": "Numerical rating (e.g., 4.5)"
    }},
  ]}}
}}
"""



class Room(BaseModel):
    """A room for selection."""
    is_available: bool = Field(
        description="Whether the room type is available for selection."
    )
    price_in_usd: int = Field(description="The cost of the room selection.")
    room_type: str = Field(
        description="Type of room, e.g. Twin with Balcon, King with Ocean View... etc."
    )


class RoomsSelection(BaseModel):
    """A list of rooms for selection."""
    rooms: list[Room]


class Hotel(BaseModel):
    """A hotel from the search."""
    name: str = Field(description="Name of the hotel")
    address: str = Field(description="Full address of the Hotel")
    check_in_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    check_out_time: str = Field(description="Time in HH:MM format, e.g. 15:30")
    thumbnail: str = Field(description="Hotel logo location")
    price: int = Field(description="Price of the room per night")


class HotelsSelection(BaseModel):
    """A list of hotels from the search."""
    hotels: list[Hotel]


class Seat(BaseModel):
    """A Seat from the search."""
    is_available: bool = Field(
        description="Whether the seat is available for selection."
    )
    price_in_usd: int = Field(description="The cost of the seat selection.")
    seat_number: str = Field(description="Seat number, e.g. 22A, 34F... etc.")


class SeatsSelection(BaseModel):
    """A list of seats from the search."""
    seats: list[list[Seat]]


class AirportEvent(BaseModel):
    """An Airport event."""
    city_name: str = Field(description="Name of the departure city")
    airport_code: str = Field(description="IATA code of the departure airport")
    timestamp: str = Field(description="ISO 8601 departure or arrival date and time")


class Flight(BaseModel):
    """A Flight search result."""
    flight_number: str = Field(
        description="Unique identifier for the flight, like BA123, AA31, etc."
    )
    departure: AirportEvent
    arrival: AirportEvent
    airlines: list[str] = Field(
        description="Airline names, e.g., American Airlines, Emirates"
    )
    airline_logo: str = Field(description="Airline logo location")
    price_in_usd: int = Field(description="Flight price in US dollars")
    number_of_stops: int = Field(description="Number of stops during the flight")


class FlightsSelection(BaseModel):
    """A list of flights from the search."""
    flights: list[Flight]


class Destination(BaseModel):
    """A destination recommendation."""
    name: str = Field(description="A Destination's Name")
    country: str = Field(description="The Destination's Country Name")
    image: str = Field(description="verified URL to an image of the destination")
    highlights: str = Field(description="Short description highlighting key features")
    rating: str = Field(description="Numerical rating (e.g., 4.5)")


class DestinationIdeas(BaseModel):
    """Destinations recommendation."""
    places: list[Destination]


class POI(BaseModel):
    """A Point Of Interest suggested by the agent."""
    place_name: str = Field(description="Name of the attraction")
    address: str = Field(
        description="An address or sufficient information to geocode for a Lat/Lon"
    )
    lat: str = Field(
        description="Numerical representation of Latitude of the location (e.g., 20.6843)"
    )
    long: str = Field(
        description="Numerical representation of Longitude of the location (e.g., -88.5678)"
    )
    review_ratings: str = Field(
        description="Numerical representation of rating (e.g. 4.8 , 3.0 , 1.0 etc)"
    )
    highlights: str = Field(description="Short description highlighting key features")
    image_url: str = Field(description="verified URL to an image of the destination")
    map_url: Optional[str] = Field(description="Verified URL to Google Map")
    place_id: Optional[str] = Field(description="Google Map place_id")


class POISuggestions(BaseModel):
    """Points of interest recommendation."""
    places: list[POI]


class AttractionEvent(BaseModel):
    """An Attraction."""
    event_type: str = Field(default="visit")
    description: str = Field(
        description="A title or description of the activity or the attraction visit"
    )
    address: str = Field(description="Full address of the attraction")
    start_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    end_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    booking_required: bool = Field(default=False)
    price: Optional[str] = Field(description="Some events may cost money")


class FlightEvent(BaseModel):
    """A Flight Segment in the itinerary."""
    event_type: str = Field(default="flight")
    description: str = Field(description="A title or description of the Flight")
    booking_required: bool = Field(default=True)
    departure_airport: str = Field(description="Airport code, i.e. SEA")
    arrival_airport: str = Field(description="Airport code, i.e. SAN")
    flight_number: str = Field(description="Flight number, e.g. UA5678")
    boarding_time: str = Field(description="Time in HH:MM format, e.g. 15:30")
    seat_number: str = Field(description="Seat Row and Position, e.g. 32A")
    departure_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    arrival_time: str = Field(description="Time in HH:MM format, e.g. 20:00")
    price: Optional[str] = Field(description="Total air fare")
    booking_id: Optional[str] = Field(
        description="Booking Reference ID, e.g LMN-012-STU"
    )


class HotelEvent(BaseModel):
    """A Hotel Booking in the itinerary."""
    event_type: str = Field(default="hotel")
    description: str = Field(description="A name, title or a description of the hotel")
    address: str = Field(description="Full address of the attraction")
    check_in_time: str = Field(description="Time in HH:MM format, e.g. 16:00")
    check_out_time: str = Field(description="Time in HH:MM format, e.g. 15:30")
    room_selection: str = Field()
    booking_required: bool = Field(default=True)
    price: Optional[str] = Field(description="Total hotel price including all nights")
    booking_id: Optional[str] = Field(
        description="Booking Reference ID, e.g ABCD12345678"
    )


class ItineraryDay(BaseModel):
    """A single day of events in the itinerary."""
    day_number: int = Field(
        description="Identify which day of the trip this represents, e.g. 1, 2, 3... etc."
    )
    date: str = Field(description="The Date this day YYYY-MM-DD format")
    events: list[Union[FlightEvent, HotelEvent, AttractionEvent]] = Field(
        default=[], description="The list of events for the day"
    )


class Itinerary(BaseModel):
    """A multi-day itinerary."""
    trip_name: str = Field(
        description="Simple one liner to describe the trip. e.g. 'San Diego to Seattle Getaway'"
    )
    start_date: str = Field(description="Trip Start Date in YYYY-MM-DD format")
    end_date: str = Field(description="Trip End Date in YYYY-MM-DD format")
    origin: str = Field(description="Trip Origin, e.g. San Diego")
    destination: str = (Field(description="Trip Destination, e.g. Seattle"),)
    days: list[ItineraryDay] = Field(
        default_factory=list, description="The multi-days itinerary"
    )


class UserProfile(BaseModel):
    """An example user profile."""
    allergies: list[str] = Field(
        default=[], description="A list of food allergies to avoid"
    )
    diet_preference: list[str] = Field(
        default=[], description="Vegetarian, Vegan... etc."
    )
    passport_nationality: str = Field(
        description="Nationality of traveler, e.g. US Citizen"
    )
    home_address: str = Field(description="Home address of traveler")
    home_transit_preference: str = Field(
        description="Preferred mode of transport around home, e.g. drive"
    )


class PackingList(BaseModel):
    """A list of things to pack for the trip."""
    items: list[str]
