import streamlit as st
import os
from dotenv import load_dotenv

# Local modules
from monte_carlo import run_monte_carlo, plot_monte_carlo
from wealth_crew import run_wealth_crew

load_dotenv()

st.set_page_config(page_title="AI Wealth Manager", layout="wide", page_icon="🏦")

st.title("🏦 AI Wealth Manager & Retirement Planner")
st.markdown("Ultimate Agentic Financial Planning using **Monte Carlo Simulations** and **CrewAI**.")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
if not api_key:
    st.sidebar.warning("API Key needed for the AI Crew.")

st.sidebar.header("📊 Your Financial Profile")
current_age = st.sidebar.number_input("Current Age", min_value=18, max_value=90, value=30)
retire_age = st.sidebar.number_input("Target Retirement Age", min_value=current_age+1, max_value=100, value=65)
current_savings = st.sidebar.number_input("Current Savings ($)", min_value=0, value=50000, step=5000)
annual_income = st.sidebar.number_input("Annual Income ($)", min_value=0, value=120000, step=5000)
annual_contribution = st.sidebar.number_input("Annual Savings Contribution ($)", min_value=0, value=15000, step=1000)
risk_profile = st.sidebar.selectbox("Risk Profile", ["Conservative", "Moderate", "Aggressive"], index=1)

years_to_retire = retire_age - current_age

# --- MAIN APP ---
if st.button("🚀 Run Comprehensive Wealth Analysis", use_container_width=True):
    # 1. Run Math Simulation
    with st.spinner(f"Running 1,000 Monte Carlo simulations over {years_to_retire} years..."):
        mc_results = run_monte_carlo(current_savings, annual_contribution, years_to_retire, risk_profile)
        
        # Display high level metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Projected Wealth (Pessimistic - 10th)", f"${mc_results['final_p10']:,.0f}")
        col2.metric("Projected Wealth (Expected - Median)", f"${mc_results['final_median']:,.0f}")
        col3.metric("Projected Wealth (Optimistic - 90th)", f"${mc_results['p90'][-1]:,.0f}")
        
        fig = plot_monte_carlo(mc_results, years_to_retire)
        st.plotly_chart(fig, use_container_width=True)
        
    # 2. Run AI Crew
    st.divider()
    st.subheader("👥 Your Dedicated Financial AI Team")
    if not api_key:
        st.error("Please provide a Gemini API key to activate the financial advisors.")
    else:
        with st.spinner("The Tax Strategist and Retirement Planner are reviewing your file..."):
            user_data = {
                'age': current_age,
                'retire_age': retire_age,
                'savings': current_savings,
                'income': annual_income,
                'contribution': annual_contribution,
                'risk': risk_profile
            }
            mc_summary = {
                'p10': mc_results['final_p10'],
                'median': mc_results['final_median'],
                'p90': mc_results['p90'][-1]
            }
            
            crew_report = run_wealth_crew(user_data, mc_summary, api_key)
            st.markdown(crew_report)
            
st.markdown("---")
st.caption("Disclaimer: This tool provides AI-driven analysis for educational purposes only. Not certified financial advice.")
