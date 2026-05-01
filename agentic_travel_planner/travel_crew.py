import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Travel Search Tool")
def search_travel(query: str) -> str:
    """Useful to search the internet for flights, weather, and local attractions."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n".join([f"Title: {r.get('title', '')}\nBody: {r.get('body', '')}" for r in results])
            return "No travel data found."
    except Exception as e:
        return f"Search failed: {e}"

def run_travel_crew(destination, days, budget, api_key):
    os.environ["GEMINI_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
    
    # 1. Logistics Agent
    logistics_agent = Agent(
        role='Chief Travel Logistician',
        goal='Understand the geography, transport options, and standard weather for the destination.',
        backstory='You are a hyper-organized travel agent who makes sure tourists do not try to visit two places on opposite sides of a city in one day.',
        verbose=True,
        allow_delegation=False,
        tools=[search_travel],
        llm=llm
    )
    
    # 2. Local Fixer Agent
    fixer_agent = Agent(
        role='Local Fixer and Culture Guide',
        goal='Find hidden gems, top-rated local restaurants, and unique cultural experiences.',
        backstory='You are a local insider. You hate tourist traps and only recommend authentic experiences.',
        verbose=True,
        allow_delegation=False,
        tools=[search_travel],
        llm=llm
    )

    # 3. Budget & Itinerary Manager
    itinerary_agent = Agent(
        role='Master Itinerary Planner',
        goal='Synthesize research into a perfect, day-by-day itinerary that fits the budget.',
        backstory='You are the master compiler. You take raw ideas and turn them into a beautiful, chronological PDF/Markdown document.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Tasks
    logistics_task = Task(
        description=f'Search for general travel logistics for {destination} for a {days}-day trip. Output the best neighborhoods to stay in and general transport advice.',
        expected_output='A markdown summary of logistics and neighborhoods.',
        agent=logistics_agent
    )
    
    fixer_task = Task(
        description=f'Based on the destination {destination}, use the Travel Search Tool to find 5 unique local experiences and 5 highly-rated local restaurants. Keep in mind the budget is: {budget}.',
        expected_output='A curated list of activities and food spots.',
        agent=fixer_agent
    )
    
    itinerary_task = Task(
        description=f'Read the logistics report and the local fixer recommendations. Create a highly detailed, chronological {days}-day itinerary for {destination}. Group activities by geographic proximity. Ensure it feels like a realistic pace.',
        expected_output='A beautiful day-by-day markdown itinerary with timestamps and location groupings.',
        agent=itinerary_agent
    )
    
    crew = Crew(
        agents=[logistics_agent, fixer_agent, itinerary_agent],
        tasks=[logistics_task, fixer_task, itinerary_task],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        return str(crew.kickoff())
    except Exception as e:
        return f"CrewAI Execution Failed: {e}"
