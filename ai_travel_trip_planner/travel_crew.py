"""
AI Travel Trip Planner — CrewAI Deep-Dive Crew
4 Specialized Agents for deep local intelligence:
  1. Budget Optimization Analyst  — cost breakdown every category
  2. Hidden Gems Scout            — off-the-beaten-path discoveries  
  3. Local Logistics Fixer        — practical getting-around tips
  4. Itinerary Synthesizer        — final beautifully compiled plan
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from duckduckgo_search import DDGS


# ── Shared Search Tool ─────────────────────────────────────────────────────────
@tool("Live Travel Search")
def live_search(query: str) -> str:
    """Search the internet in real-time for travel information, prices, tips and local insights."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if results:
                return "\n\n".join([
                    f"**{r.get('title', '')}**\n{r.get('body', '')}"
                    for r in results
                ])
            return "No results found for this query."
    except Exception as e:
        return f"Search failed: {e}"


def run_travel_crew(destination: str, days: int, budget: str, api_key: str) -> str:
    """
    Run the full CrewAI travel intelligence crew for deep local expertise.
    Returns a comprehensive markdown report.
    """
    os.environ["GEMINI_API_KEY"] = api_key
    os.environ["GOOGLE_API_KEY"] = api_key

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=api_key,
        temperature=0.7,
    )

    # ── Agent 1: Budget Optimization Analyst ──────────────────────────────────
    budget_agent = Agent(
        role="Expert Travel Budget Optimization Analyst",
        goal=(
            "Search the internet and provide a COMPLETE, realistic cost breakdown "
            f"for a {days}-day trip to {destination} for budget: {budget}. "
            "Cover flights, accommodation, food, transport, activities, visa fees, insurance."
        ),
        backstory=(
            "You are a certified travel financial advisor who has planned trips to 150+ countries. "
            "You know exact price ranges, seasonal fluctuations, and money-saving hacks that most "
            "travel blogs miss. You always provide specific numbers, not vague estimates."
        ),
        tools=[live_search],
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    # ── Agent 2: Hidden Gems & Experience Scout ────────────────────────────────
    gems_agent = Agent(
        role="Elite Hidden Gems & Authentic Experience Scout",
        goal=(
            f"Search the internet to find the TOP hidden gems, local secrets, and authentic "
            f"experiences in {destination} that most tourists NEVER discover. "
            "Find off-the-beaten-path locations, local-only restaurants, secret viewpoints, "
            "underground events, and experiences that make a trip truly unforgettable."
        ),
        backstory=(
            "You are a seasoned travel journalist who has lived in 40 countries and writes for "
            "National Geographic and Condé Nast Traveler. You despise tourist traps and only "
            "recommend places that locals actually love. Your tips are gold."
        ),
        tools=[live_search],
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    # ── Agent 3: Local Logistics Fixer ────────────────────────────────────────
    fixer_agent = Agent(
        role="Master Local Logistics & Practical Travel Fixer",
        goal=(
            f"Search the internet and provide ALL practical logistics for visiting {destination}: "
            "SIM cards & internet access, money ATMs & exchange, pharmacy & hospital locations, "
            "local apps to download, useful phone numbers, neighborhood safety, common scams, "
            "photography rules, power adapters, and any OTHER practical survival tips."
        ),
        backstory=(
            "You are the person every traveler wishes they had — a hyper-organized local contact "
            "who knows every practical detail. You've rescued hundreds of stranded travelers. "
            "Your specialty is turning travel chaos into seamless adventures."
        ),
        tools=[live_search],
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    # ── Agent 4: Master Itinerary Synthesizer ─────────────────────────────────
    synthesizer_agent = Agent(
        role="Master Travel Itinerary Synthesizer & Experience Curator",
        goal=(
            f"Read all research from the Budget Analyst, Hidden Gems Scout, and Local Fixer. "
            f"Create the most BEAUTIFUL and COMPREHENSIVE {days}-day itinerary for {destination} "
            "that weaves together budget wisdom, hidden gems, and practical logistics into a "
            "perfect, actionable travel plan."
        ),
        backstory=(
            "You are the head concierge of the world's best luxury travel agency. "
            "You've crafted bespoke itineraries for royalty, celebrities, and discerning travelers. "
            "You know that a great itinerary balances discovery, rest, food, culture, and spontaneity. "
            "Your plans are works of art."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    # ── Task 1: Budget Breakdown ───────────────────────────────────────────────
    budget_task = Task(
        description=(
            f"Research and create a COMPLETE cost breakdown for {days} days in {destination}. "
            f"Budget target: {budget}.\n\n"
            "Use the Live Travel Search tool to find CURRENT prices. Include:\n"
            "1. Flights: estimated round-trip cost and best booking strategy\n"
            "2. Accommodation: price per night across 3 budget tiers\n"
            "3. Food: daily food budget (street food / mid-range / fine dining)\n"
            "4. Local Transport: daily transport cost\n"
            "5. Activities & Entrance Fees: key attraction costs\n"
            "6. Visa & Insurance: fees if applicable\n"
            "7. Miscellaneous: shopping, tips, emergencies\n"
            "8. TOTAL ESTIMATED COST for the entire trip\n"
            "9. Top 5 money-saving hacks specific to this destination"
        ),
        expected_output=(
            "A beautiful markdown cost breakdown table with all categories, "
            "real price ranges, totals, and actionable money-saving tips."
        ),
        agent=budget_agent,
    )

    # ── Task 2: Hidden Gems ────────────────────────────────────────────────────
    gems_task = Task(
        description=(
            f"Search the internet to discover the TOP hidden gems and authentic local experiences "
            f"in {destination} for a {days}-day trip. Find:\n"
            "1. 5 secret/off-the-beaten-path locations tourists never find\n"
            "2. 3 local-only restaurants or food stalls (with dish names)\n"
            "3. 2 unique cultural experiences available only here\n"
            "4. 3 best day trips from the city\n"
            "5. Best local market or bazaar and what to buy\n"
            "6. Best time of day for key attractions (beat the crowds)\n"
            "7. Local festivals/events happening during typical travel periods\n"
            "8. Instagram-worthy spots that aren't overrun with tourists"
        ),
        expected_output=(
            "A rich, detailed markdown guide to hidden gems with specific names, "
            "addresses/locations, what makes each special, and practical tips to visit them."
        ),
        agent=gems_agent,
    )

    # ── Task 3: Practical Logistics ────────────────────────────────────────────
    fixer_task = Task(
        description=(
            f"Research and compile ALL practical survival information for visiting {destination}:\n"
            "1. SIM Card: best local SIM/eSIM options with prices and data plans\n"
            "2. Money: best ATMs, exchange bureaus, avoid-these-traps, ideal cash amount\n"
            "3. Connectivity: best apps to download before arriving (maps, transport, food delivery)\n"
            "4. Safety: neighborhood safety map, common tourist scams and how to avoid them\n"
            "5. Health: nearest hospitals, pharmacy chains, required/recommended vaccines\n"
            "6. Emergency Numbers: police, ambulance, embassy contacts for major nationalities\n"
            "7. Power & Tech: plug type, voltage, adapter needed\n"
            "8. Communication: useful local phrases, do translation apps work well here\n"
            "9. Photography Rules: what you can/cannot photograph\n"
            "10. Any destination-specific quirks tourists must know"
        ),
        expected_output=(
            "A comprehensive practical guide in clean markdown with sections for each category, "
            "specific app names, phone numbers, and actionable advice."
        ),
        agent=fixer_agent,
    )

    # ── Task 4: Final Itinerary ────────────────────────────────────────────────
    itinerary_task = Task(
        description=(
            f"Using the budget analysis, hidden gems research, and practical logistics, "
            f"create the ULTIMATE {days}-day travel itinerary for {destination}.\n\n"
            "Structure each day as:\n"
            "**Day X — [Creative Day Theme Title]**\n"
            "- 🌅 Morning (7-12pm): [Activities with transport instructions and costs]\n"
            "- ☀️ Afternoon (12-6pm): [Activities + lunch recommendation]\n"  
            "- 🌙 Evening (6pm+): [Dinner + evening activity]\n"
            "- 💡 Pro Tip for the day\n"
            "- 💰 Estimated spend for the day\n\n"
            "After the daily itinerary, include:\n"
            "- 📦 Complete Packing List\n"
            "- 💳 Budget Summary Table\n"
            "- 🗺️ Neighborhood Guide (which area to stay in for what)\n"
            "- 🚨 Emergency Contacts\n"
            "- ⭐ Top 3 Absolute Must-Dos"
        ),
        expected_output=(
            "A stunning, publication-quality markdown itinerary that covers every single "
            "day with timing, costs, transport, food, hidden gems, and practical tips. "
            "This should be the best travel guide the user has ever seen."
        ),
        agent=synthesizer_agent,
    )

    # ── Crew ───────────────────────────────────────────────────────────────────
    crew = Crew(
        agents=[budget_agent, gems_agent, fixer_agent, synthesizer_agent],
        tasks=[budget_task, gems_task, fixer_task, itinerary_task],
        process=Process.sequential,
        verbose=False,
    )

    try:
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        return f"❌ CrewAI execution failed: {e}"
