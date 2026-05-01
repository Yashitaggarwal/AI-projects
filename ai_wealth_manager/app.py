import streamlit as st
import os
from dotenv import load_dotenv

# Local modules
from monte_carlo import run_monte_carlo, plot_monte_carlo
from wealth_crew import run_wealth_crew

load_dotenv()

st.set_page_config(page_title="AI Wealth Manager", layout="wide", page_icon="🏦")

# Premium Custom CSS
st.markdown("""
<style>
    /* Global dark theme and typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Header styling with animated gradient */
    h1 {
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: pulse 2s infinite alternate;
    }
    
    @keyframes pulse {
        0% { opacity: 0.8; }
        100% { opacity: 1; text-shadow: 0 0 20px rgba(79,172,254,0.5); }
    }
    
    /* Subtitle styling */
    .stMarkdown p {
        font-size: 1.1rem;
        color: #cbd5e1;
        text-align: center;
    }
    
    /* Sidebar styling - Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #4facfe;
        box-shadow: 0 0 10px rgba(79,172,254,0.3);
    }
    
    /* Selectbox */
    .stSelectbox>div>div>div {
        background: rgba(255, 255, 255, 0.05);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #0f172a !important;
        font-weight: 700;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,242,254,0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,242,254,0.6);
    }
    
    /* Metrics Cards */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: rgba(79,172,254,0.5);
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00f2fe;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏦 AI Wealth Manager</h1>", unsafe_allow_html=True)
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
