import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Web Search Tool")
def search_web(query: str) -> str:
    """Useful to search the internet for news, earnings, and financial data."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n".join([f"Title: {r.get('title', '')}\nBody: {r.get('body', '')}" for r in results])
            return "No recent news found."
    except Exception as e:
        return f"Search failed: {e}"

def run_crewai_analysis(ticker, api_key):
    """
    Runs a full CrewAI workflow.
    Note: CrewAI execution can take 30-60 seconds as agents autonomously search the web.
    """
    os.environ["GEMINI_API_KEY"] = api_key
    # We use a robust model for agent routing
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
    
    # 1. Fundamental Analyst
    fundamental_analyst = Agent(
        role='Senior Fundamental Analyst',
        goal=f'Uncover the macroeconomic drivers, earnings sentiment, and news catalysts for {ticker}',
        backstory='You are a seasoned analyst at a top hedge fund known for finding hidden value. You rely heavily on web searches to find the latest data.',
        verbose=True,
        allow_delegation=False,
        tools=[search_web],
        llm=llm
    )
    
    # 2. Risk Manager
    risk_manager = Agent(
        role='Chief Risk Officer',
        goal=f'Identify potential down-side risks, macro headwinds, and suggest risk mitigation for {ticker}',
        backstory='You protect the firm\'s capital. You are naturally skeptical and look for holes in bullish theses. You search for negative catalysts.',
        verbose=True,
        allow_delegation=False,
        tools=[search_web],
        llm=llm
    )
    
    # Tasks
    research_task = Task(
        description=f'Search the web for the latest news, earnings reports, and market sentiment regarding {ticker}. Summarize the bullish and bearish fundamental factors.',
        expected_output=f'A comprehensive fundamental report on {ticker} highlighting catalysts and earnings potential.',
        agent=fundamental_analyst
    )
    
    risk_task = Task(
        description=f'Based on the fundamental research, actively search for specific risks (regulatory, competition, macro) regarding {ticker}. Define the risk profile.',
        expected_output=f'A detailed risk assessment for {ticker} including a final Risk Rating (Low/Med/High).',
        agent=risk_manager
    )
    
    # Crew
    crew = Crew(
        agents=[fundamental_analyst, risk_manager],
        tasks=[research_task, risk_task],
        process=Process.sequential,
        verbose=False # Set to false to avoid polluting stdout too much in production
    )
    
    try:
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        return f"CrewAI Execution Failed: {e}"
