import streamlit as st
import os
from dotenv import load_dotenv
from product_crew import run_product_crew

load_dotenv()

st.set_page_config(page_title="AI Co-Founder", layout="centered", page_icon="💡")

# Premium Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top, #1a1025 0%, #050510 100%);
        color: #e2e8f0;
    }
    
    /* Glowing Header */
    h1 {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 4rem !important;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
        filter: drop-shadow(0 0 10px rgba(168,85,247,0.4));
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #cbd5e1;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 10, 25, 0.7) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(168,85,247,0.2);
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03);
        color: #fff;
        border: 1px solid rgba(168,85,247,0.3);
        border-radius: 12px;
        font-size: 1.1rem;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #ec4899;
        box-shadow: 0 0 20px rgba(236,72,153,0.3);
    }
    
    /* Glow Button */
    .stButton>button {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
        color: white !important;
        font-weight: 600;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(236,72,153,0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(168,85,247,0.7);
    }
    
    /* Markdown Output Container */
    .stMarkdown {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💡 AI Co-Founder</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter your raw startup idea and let a team of AI experts write your PRD, analyze the market, and design your tech stack.</p>", unsafe_allow_html=True)

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
