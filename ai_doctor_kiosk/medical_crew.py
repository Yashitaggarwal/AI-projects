import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

def run_medical_crew(patient_age, patient_gender, symptoms, duration, api_key):
    os.environ["GEMINI_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
    
    # 1. Triage Nurse
    triage_agent = Agent(
        role='ER Triage Nurse',
        goal='Standardize patient symptoms into a clear clinical format and establish the timeline.',
        backstory='You are a veteran ER nurse who excels at extracting the timeline and severity of symptoms from panicked patients.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # 2. Safety Officer (Red Flag Detector)
    safety_agent = Agent(
        role='Medical Safety Officer',
        goal='Identify life-threatening "Red Flag" symptoms (e.g., chest pain, sudden numbness, severe shortness of breath).',
        backstory='Your only job is risk mitigation. If you see a red flag, you escalate immediately.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 3. Diagnostician
    diagnostician_agent = Agent(
        role='Chief Diagnostic Specialist',
        goal='Generate a Differential Diagnosis (top 3 likely conditions) based on the nurse\'s report.',
        backstory='You are a world-renowned diagnostician, like Dr. House, but with better bedside manner. You think probabilistically.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Patient Context
    patient_context = f"""
    --- PATIENT INTAKE ---
    Age: {patient_age}
    Gender: {patient_gender}
    Reported Symptoms: "{symptoms}"
    Symptom Duration: {duration}
    """
    
    # Tasks
    triage_task = Task(
        description=f'Review the patient intake:\n{patient_context}\n\nRewrite these symptoms into a professional clinical summary.',
        expected_output='A concise clinical summary paragraph.',
        agent=triage_agent
    )
    
    safety_task = Task(
        description=f'Review the clinical summary. Are there ANY red flags (cardiac, neurological, severe respiratory)? If YES, output a bold WARNING. If NO, state "No immediate red flags detected."',
        expected_output='A safety assessment block with either a warning or clearance.',
        agent=safety_agent
    )
    
    diagnostic_task = Task(
        description=f'Review the clinical summary and the safety assessment. Generate a Differential Diagnosis. List the top 3 most likely conditions, explaining why they fit the symptoms. Include a "Next Steps" section (e.g., rest, see a PCP, or go to the ER).',
        expected_output='A beautifully formatted markdown medical report containing the clinical summary, safety assessment, differential diagnosis, and next steps.',
        agent=diagnostician_agent
    )
    
    crew = Crew(
        agents=[triage_agent, safety_agent, diagnostician_agent],
        tasks=[triage_task, safety_task, diagnostic_task],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        return str(crew.kickoff())
    except Exception as e:
        return f"CrewAI Execution Failed: {e}"
