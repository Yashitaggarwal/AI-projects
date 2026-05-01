import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

def run_wealth_crew(user_data, mc_results_summary, api_key):
    """
    Runs the AI Wealth Manager crew.
    """
    os.environ["GEMINI_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
    
    # 1. Tax & Optimization Strategist
    tax_strategist = Agent(
        role='Senior Tax & Wealth Strategist',
        goal='Analyze income and assets to minimize tax burden and maximize tax-advantaged growth.',
        backstory='You are a CPA and CFP who specializes in tax-loss harvesting, backdoor Roths, and optimizing savings rate allocation.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # 2. Retirement Planner
    retirement_planner = Agent(
        role='Certified Financial Planner (CFP)',
        goal='Evaluate the Monte Carlo simulations against the user\'s goals and suggest actionable portfolio changes.',
        backstory='You are a behavioral finance expert. You look at mathematical projections and translate them into human-readable advice.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Context string
    context = f"""
    --- USER FINANCIAL PROFILE ---
    Age: {user_data.get('age')}
    Target Retirement Age: {user_data.get('retire_age')}
    Current Savings: ${user_data.get('savings'):,}
    Annual Income: ${user_data.get('income'):,}
    Annual Savings Contribution: ${user_data.get('contribution'):,}
    Risk Profile: {user_data.get('risk')}
    
    --- MONTE CARLO PROJECTIONS (At Retirement Age) ---
    Optimistic Scenario (90th Percentile): ${mc_results_summary.get('p90'):,.2f}
    Expected Scenario (Median): ${mc_results_summary.get('median'):,.2f}
    Pessimistic Scenario (10th Percentile): ${mc_results_summary.get('p10'):,.2f}
    """
    
    # Tasks
    tax_task = Task(
        description=f'Review the following user profile:\n{context}\n\nSuggest 3 specific, actionable tax optimization or account-allocation strategies (e.g., 401k, IRA, HSA) based on their income and savings rate.',
        expected_output='A clear, bulleted list of tax and savings optimizations tailored to the user. Format with markdown headers.',
        agent=tax_strategist
    )
    
    retirement_task = Task(
        description=f'Review the user profile and Monte Carlo projections:\n{context}\n\nRead the Tax Strategist\'s suggestions. Assess if the user is on track to retire comfortably. If the pessimistic scenario is too low, suggest how much more they need to save or if they should adjust their risk profile. Provide a holistic final summary.',
        expected_output='A comprehensive retirement readiness report and final verdict on their trajectory, formatted beautifully in markdown.',
        agent=retirement_planner
    )
    
    # Crew
    crew = Crew(
        agents=[tax_strategist, retirement_planner],
        tasks=[tax_task, retirement_task],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        return f"CrewAI Execution Failed: {e}"
