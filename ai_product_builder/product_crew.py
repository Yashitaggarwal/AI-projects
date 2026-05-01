import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Market Research Tool")
def search_market(query: str) -> str:
    """Useful to search the internet for competitor analysis and market trends."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n".join([f"Title: {r.get('title', '')}\nBody: {r.get('body', '')}" for r in results])
            return "No market data found."
    except Exception as e:
        return f"Search failed: {e}"

def run_product_crew(idea, api_key):
    os.environ["GEMINI_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
    
    # 1. Market Researcher
    researcher_agent = Agent(
        role='Market Intelligence Lead',
        goal='Analyze the current market landscape for the proposed idea and identify key competitors.',
        backstory='You are obsessed with competitive moats and market sizing.',
        verbose=True,
        allow_delegation=False,
        tools=[search_market],
        llm=llm
    )
    
    # 2. Product Manager
    pm_agent = Agent(
        role='Chief Product Officer',
        goal='Define the core value proposition and write a comprehensive Product Requirements Document (PRD).',
        backstory='You are a visionary product manager who has launched several unicorns. You focus on user needs and core loops.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 3. System Architect
    architect_agent = Agent(
        role='Lead Systems Architect',
        goal='Design the technical stack and high-level architecture needed to build this product.',
        backstory='You are a pragmatic engineer who chooses boring, scalable tech to get the job done fast.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Tasks
    research_task = Task(
        description=f'Use the Market Research Tool to search the web for competitors related to this startup idea: "{idea}". Output a competitive analysis report.',
        expected_output='A markdown report detailing 3 potential competitors and the market opportunity.',
        agent=researcher_agent
    )
    
    prd_task = Task(
        description=f'Based on the competitive analysis and the raw idea "{idea}", write a comprehensive PRD. Define the target user, the "aha" moment, and the MVP feature set.',
        expected_output='A well-structured PRD with clear feature lists and user personas.',
        agent=pm_agent
    )
    
    tech_task = Task(
        description=f'Read the PRD. Design the optimal tech stack (Frontend, Backend, Database, AI APIs) required to build this MVP over a weekend. Explain why you chose these technologies.',
        expected_output='A technical architecture document detailing the tech stack and data models.',
        agent=architect_agent
    )
    
    crew = Crew(
        agents=[researcher_agent, pm_agent, architect_agent],
        tasks=[research_task, prd_task, tech_task],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        return str(crew.kickoff())
    except Exception as e:
        return f"CrewAI Execution Failed: {e}"
