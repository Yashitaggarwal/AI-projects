import streamlit as st
import os
from dotenv import load_dotenv
from product_crew import run_product_crew

load_dotenv()

st.set_page_config(page_title="AI Co-Founder", layout="centered", page_icon="💡")

st.title("💡 AI Co-Founder & Product Builder")
st.markdown("Enter your raw startup idea and let a team of AI experts write your PRD, analyze the market, and design your tech stack.")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
if not api_key:
    st.sidebar.warning("API Key needed for the AI Crew.")

# --- MAIN APP ---
idea = st.text_area("Your Startup Idea", placeholder="e.g., An Uber for dog walking that connects busy owners with vetted walkers in under 10 minutes.")

if st.button("🚀 Generate Startup Business Plan", use_container_width=True):
    if not idea:
        st.error("Please enter an idea.")
    elif not api_key:
        st.error("Please provide a Gemini API key.")
    else:
        with st.spinner("Your AI team (Market Researcher, CPO, and Architect) are working. This usually takes 30-60 seconds..."):
            crew_report = run_product_crew(idea, api_key)
            st.divider()
            st.markdown("### 🏆 Co-Founder Master Plan")
            st.markdown(crew_report)
            
st.markdown("---")
st.caption("Disclaimer: This tool provides AI-driven analysis for educational purposes only.")
