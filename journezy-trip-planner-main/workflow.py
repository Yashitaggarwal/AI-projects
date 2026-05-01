import os
import asyncio
from typing import Any, Dict

# Agno Imports
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGo

class TourPlannerWorkflow:
    def __init__(self, language: str = "en"):
        self.language = language
        
        # We will attempt to get the API key.
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            print("⚠️ [AGNO-WORKFLOW] No Gemini API key found in environment!")
            
        # Define the underlying Gemini model
        self.model = Gemini(id="gemini-1.5-pro", api_key=self.api_key)
        
        # Initialize specialized Agents
        self.logistics_agent = Agent(
            name="Chief Travel Logistician",
            role="Research flights, travel times, optimal routes, and weather.",
            model=self.model,
            tools=[DuckDuckGo()],
            instructions=[
                "Use DuckDuckGo to search for realistic travel times and transit options.",
                "Always check the typical weather for the destination during the travel dates.",
                "Ensure that you do not recommend two locations on opposite sides of a city on the same day."
            ],
            markdown=True,
            show_tool_calls=True
        )
        
        self.local_expert_agent = Agent(
            name="Local Culture & Dining Expert",
            role="Find highly-rated, authentic restaurants and unique experiences.",
            model=self.model,
            tools=[DuckDuckGo()],
            instructions=[
                "Use DuckDuckGo to search for top-rated local food and hidden gems.",
                "Tailor your recommendations STRICTLY to the user's budget and traveler profile.",
                "Avoid tourist traps. Provide specific names of restaurants and attractions."
            ],
            markdown=True,
            show_tool_calls=True
        )
        
        self.master_planner_agent = Agent(
            name="Senior Itinerary Director",
            role="Compile research into a final day-by-day markdown itinerary.",
            model=self.model,
            instructions=[
                "Collaborate with the Logistician and Local Expert.",
                "Synthesize their findings into a cohesive, chronological itinerary.",
                "Format the final output strictly as beautiful, readable Markdown.",
                "Group activities by geographic proximity.",
                f"Ensure the final output is written in language code: {self.language}."
            ],
            markdown=True
        )
        
        # Create the collaborative Agno Team
        self.travel_team = Team(
            name="Journezy Ultimate Travel Team",
            model=self.model,
            members=[self.logistics_agent, self.local_expert_agent, self.master_planner_agent],
            instructions=[
                "You are an elite, highly paid concierge team.",
                "Work together to plan the perfect trip.",
                "The Logistician must provide transit and weather data.",
                "The Local Expert must provide specific dining and activity spots.",
                "The Master Planner MUST output the final response as a detailed Day-by-Day Markdown itinerary."
            ],
            delegate_to_all_members=True,
            markdown=True
        )
        
        # Placeholders to satisfy any legacy attributes `main.py` might try to read
        self.flights_data = {"status": "Agentic Search Used"}
        self.hotels_data = {"status": "Agentic Search Used"}
        self.places_data = {"status": "Agentic Search Used"}
        self.itinerary = {"status": "Agentic Search Used"}

    async def run(self, query: str, budget_amount: float = None, currency: str = "USD", 
                  travelers: Any = None, flight_preferences: Any = None, 
                  consider_toddler_friendly: bool = False, 
                  consider_senior_friendly: bool = False, 
                  safety_check: bool = True) -> str:
        """
        Executes the Agno Team to generate the itinerary based on the structured query.
        """
        print(f"🚀 [AGNO-WORKFLOW] Starting Agentic Team Execution for query: {query[:50]}...")
        
        # Reconstruct context for the team
        context = f"""
        Please plan a trip based on this detailed prompt:
        {query}
        
        Constraints:
        - Budget: {budget_amount} {currency}
        - Toddler Friendly Required: {consider_toddler_friendly}
        - Senior Friendly Required: {consider_senior_friendly}
        """
        
        try:
            # We run it in a thread because Agno's `run` is synchronous 
            # and FastAPI expects `run` to not block the event loop entirely.
            loop = asyncio.get_event_loop()
            
            # Using run() method of Team (in Agno v2 it's run or print_response)
            response = await loop.run_in_executor(
                None, 
                lambda: self.travel_team.run(context)
            )
            
            print("✅ [AGNO-WORKFLOW] Team Execution Complete.")
            
            # response.content contains the final string
            return response.content
            
        except Exception as e:
            print(f"❌ [AGNO-WORKFLOW] Error during Team execution: {e}")
            return f"Error: The Agentic Team failed to generate the itinerary due to: {str(e)}"
