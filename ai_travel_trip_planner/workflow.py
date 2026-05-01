"""
AI Travel Trip Planner — Ultimate Agno Multi-Agent Workflow
7 Specialized Agents covering EVERY aspect of travel:
  1. Flight Intelligence      — live routes, prices, best booking windows
  2. Accommodation Scout      — hotels, hostels, neighborhoods
  3. Ground Transport         — airport transfers, metro, trains, car rental
  4. Cultural Intelligence    — visa, customs, currency, language, etiquette
  5. Food & Experience Expert — must-eat dishes, restaurants, markets, nightlife
  6. Weather & Packing        — forecasts, packing lists, best travel season
  7. Master Itinerary Director— synthesizes everything into final day-by-day plan
"""

import os
import asyncio
from typing import Any, Optional

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGo


class TourPlannerWorkflow:
    """Ultimate 7-agent Agno travel planning team."""

    def __init__(self, language: str = "en"):
        self.language = language
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY / GOOGLE_API_KEY not set.")

        model = Gemini(id="gemini-1.5-pro", api_key=self.api_key)
        search = DuckDuckGo()

        # ── Agent 1 : Travel Access & Route Intelligence ─────────────────────
        self.flight_agent = Agent(
            name="Travel Access & Route Intelligence Specialist",
            role="Discover EVERY possible way to reach the destination — flights, trains, ferries, buses, roads, or multi-modal combos.",
            model=model,
            tools=[search],
            instructions=[
                "FIRST determine what transport modes actually EXIST for this route (not every destination has an airport).",
                "Cover ALL viable options: direct flights, connecting flights, high-speed trains, overnight trains, intercity buses, ferries, cruise ships, road trips, and multi-modal combos.",
                "For each option provide: duration, approximate price range in the user's currency, booking platforms, pros and cons.",
                "If no direct flights exist, explain the best multi-leg options and layover strategies.",
                "For trains: mention booking platforms (Eurail, IRCTC, JR Pass, etc.) and reservation tips.",
                "For ferries/boats: mention schedules, cabin vs deck options, booking lead time.",
                "For road trips: mention border crossing rules, road conditions, required documents, fuel costs.",
                "Always state which option is BEST for the budget, speed, and comfort level.",
                "Include baggage norms and check-in tips for whichever modes apply.",
                "Note any visa requirements at transit points regardless of transport mode.",
            ],
            markdown=True,
            show_tool_calls=True,
        )

        # ── Agent 2 : Accommodation Scout ─────────────────────────────────────
        self.hotel_agent = Agent(
            name="Accommodation Intelligence Scout",
            role="Find the best places to stay for every budget level.",
            model=model,
            tools=[search],
            instructions=[
                "Search for the best neighborhoods to stay in for tourists.",
                "Provide 3 tiers: Budget (hostels/guesthouses), Mid-range, and Luxury hotels.",
                "Include approximate price per night in the user's currency.",
                "Name specific recommended hotels/hostels with their pros.",
                "Mention which areas to AVOID and why (safety, noise, tourist traps).",
                "Include tips on booking platforms (Booking.com vs Airbnb vs direct).",
                "Flag any local laws about short-term rentals if relevant.",
            ],
            markdown=True,
            show_tool_calls=True,
        )

        # ── Agent 3 : Ground Transport Expert ────────────────────────────────
        self.transport_agent = Agent(
            name="Ground Transport & Logistics Expert",
            role="Plan every local movement — airport to city, inter-city, daily transport.",
            model=model,
            tools=[search],
            instructions=[
                "Explain ALL options for getting from the airport to the city center (taxi, metro, bus, train, shuttle) with prices and durations.",
                "Describe the local public transport system (metro lines, buses, trams, ferries).",
                "Recommend transport apps used locally (e.g., Grab, Bolt, local apps).",
                "Include car rental tips if useful (international driving license, left/right-hand drive, toll systems).",
                "Mention ride-hailing apps available at the destination.",
                "For multi-city itineraries, include inter-city train/bus options.",
                "Provide practical tips: peak hours to avoid, safety on public transport.",
            ],
            markdown=True,
            show_tool_calls=True,
        )

        # ── Agent 4 : Cultural Intelligence Officer ───────────────────────────
        self.culture_agent = Agent(
            name="Cultural Intelligence & Visa Officer",
            role="Provide ALL essential cultural, legal, visa, currency and safety information.",
            model=model,
            tools=[search],
            instructions=[
                "State the visa requirements for the MOST COMMON passport holders (US, UK, EU, Indian).",
                "Explain the currency: name, exchange rate vs USD, where to exchange, ATM availability.",
                "List the top 5 cultural dos and DON'Ts at the destination.",
                "Mention local laws tourists commonly break (drugs, photography, dress codes, alcohol).",
                "Note the official language and 10 useful local phrases with pronunciation.",
                "Explain tipping culture and expected tip percentages.",
                "Mention religious customs and sacred site etiquette.",
                "Include emergency numbers: police, ambulance, tourist helpline.",
            ],
            markdown=True,
            show_tool_calls=True,
        )

        # ── Agent 5 : Food & Experience Expert ────────────────────────────────
        self.food_agent = Agent(
            name="Food & Experience Intelligence Expert",
            role="Uncover the best food, markets, nightlife and unique experiences.",
            model=model,
            tools=[search],
            instructions=[
                "List the 10 MUST-EAT local dishes with brief descriptions.",
                "Recommend 3 budget street food spots, 3 mid-range restaurants, 2 fine dining options.",
                "Mention local markets, food halls, and night markets.",
                "List top 5 unique experiences NOT found in guidebooks (hidden gems).",
                "Include day trips from the destination worth doing.",
                "Mention local festivals or events that might coincide with the travel dates.",
                "Flag common food scams or tourist traps to avoid.",
                "Note vegetarian/vegan/halal/kosher food availability.",
            ],
            markdown=True,
            show_tool_calls=True,
        )

        # ── Agent 6 : Weather, Health & Packing Advisor ───────────────────────
        self.weather_agent = Agent(
            name="Weather, Health & Packing Intelligence Advisor",
            role="Provide weather forecasts, health advisories, and a tailored packing list.",
            model=model,
            tools=[search],
            instructions=[
                "Describe the typical weather during the travel dates (temperature range, rainfall, humidity).",
                "Rate whether this is the BEST, GOOD, or OFF season to visit — explain why.",
                "List any health risks: vaccinations recommended, malaria zones, water safety.",
                "Provide a COMPLETE packing list tailored to the destination, season, and trip duration.",
                "Include specific clothing recommendations (dress codes, layers, footwear).",
                "List essential items specific to this destination (adapter plugs, bug spray, sunscreen SPF).",
                "Mention travel insurance recommendations and what to look for in a policy.",
                "Note any altitude sickness risk if applicable.",
            ],
            markdown=True,
            show_tool_calls=True,
        )

        # ── Agent 7 : Master Itinerary Director ───────────────────────────────
        self.itinerary_agent = Agent(
            name="Master Itinerary Director",
            role="Synthesize ALL agent research into the perfect day-by-day travel plan.",
            model=model,
            instructions=[
                "Read ALL the research from the other agents.",
                "Create a DETAILED, hour-by-hour day-by-day itinerary.",
                "Group activities by geographic proximity to minimize travel time.",
                "Include: morning, afternoon, and evening plans for each day.",
                "Embed transport tips (how to get from A to B with duration and cost).",
                "Include meal recommendations for breakfast, lunch, and dinner each day.",
                "Add a 'Travel Tips for Today' box for each day.",
                "Build in free time and rest periods — do NOT overload the schedule.",
                "Include a BUDGET BREAKDOWN: estimated daily spend by category.",
                "End with a MASTER PACKING CHECKLIST.",
                f"Write the ENTIRE output in language code: {language}.",
                "Format beautifully with Markdown headers, emojis, and tables.",
            ],
            markdown=True,
        )

        # ── Agno Team ──────────────────────────────────────────────────────────
        self.travel_team = Team(
            name="Ultimate AI Travel Intelligence Team",
            model=model,
            members=[
                self.flight_agent,  # now covers ALL transport modes
                self.hotel_agent,
                self.transport_agent,
                self.culture_agent,
                self.food_agent,
                self.weather_agent,
                self.itinerary_agent,
            ],
            instructions=[
                "You are the world's most elite travel concierge team.",
                "Each specialist agent must contribute their domain expertise.",
                "The Master Itinerary Director must synthesize ALL research into a unified final plan.",
                "Leave NO detail uncovered: flights, hotels, transport, culture, food, weather, packing.",
                "The final output MUST be comprehensive, beautiful markdown.",
            ],
            delegate_to_all_members=True,
            markdown=True,
        )

        # Placeholders for legacy attribute compatibility
        self.itinerary = None
        self.flights_data = None
        self.hotels_data = None
        self.places_data = None

    async def run(
        self,
        query: str,
        budget_amount: Optional[float] = None,
        currency: str = "USD",
        travelers: Any = None,
        flight_preferences: Any = None,
        consider_toddler_friendly: bool = False,
        consider_senior_friendly: bool = False,
        safety_check: bool = True,
    ) -> str:
        """Execute the full 7-agent travel planning team."""

        context = f"""
You are the world's best travel concierge team. Plan the MOST COMPREHENSIVE trip possible.

USER REQUEST:
{query}

TRIP CONSTRAINTS:
- Budget: {budget_amount} {currency} (total). If 0 or None, provide options for all budget levels.
- Currency preferred: {currency}
- Toddler-Friendly Required: {consider_toddler_friendly}
- Senior-Accessible Required: {consider_senior_friendly}
- Safety Assessment Required: {safety_check}

TRAVELER PROFILE:
{f"- Adults: {travelers.adults}" if travelers else ""}
{f"- Children (5-17): {travelers.children}" if travelers else ""}
{f"- Seniors (65+): {travelers.seniors}" if travelers else ""}
{f"- Toddlers (<5): {travelers.children_under_5}" if travelers else ""}

FLIGHT PREFERENCES:
{f"- Avoid red-eye flights: {flight_preferences.avoid_red_eye}" if flight_preferences else ""}
{f"- Avoid early morning: {flight_preferences.avoid_early_morning}" if flight_preferences else ""}
{f"- Direct flights only: {flight_preferences.direct_flights_only}" if flight_preferences else ""}

MANDATE: Every agent must search the internet for REAL, CURRENT information.
Cover: Flights · Hotels · Ground Transport · Visa & Currency · Culture & Language · 
Food & Hidden Gems · Weather & Packing · Health & Safety · Day-by-Day Itinerary · Budget Breakdown.
"""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.travel_team.run(context)
            )
            content = response.content if hasattr(response, "content") else str(response)
            self.itinerary = content
            return content
        except Exception as e:
            err = f"❌ Agno team error: {e}"
            self.itinerary = err
            return err
