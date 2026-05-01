import streamlit as st
import os
from dotenv import load_dotenv
from medical_crew import run_medical_crew

load_dotenv()

st.set_page_config(page_title="AI Doctor Kiosk", layout="centered", page_icon="🩺")

# Premium Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Clinical Header */
    h1 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-align: center;
        border-bottom: 2px solid rgba(56,189,248,0.2);
        padding-bottom: 1rem;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #94a3b8;
        background: rgba(239, 68, 68, 0.1);
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid rgba(239,68,68,0.2);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea textarea, .stSelectbox>div>div>div {
        background: rgba(255, 255, 255, 0.03);
        color: #e2e8f0;
        border: 1px solid rgba(56,189,248,0.3);
        border-radius: 6px;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 10px rgba(56,189,248,0.2);
    }
    
    /* Warning Button */
    .stButton>button {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        color: white !important;
        font-weight: 700;
        border: none;
        padding: 1rem;
        border-radius: 8px;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(239,68,68,0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(239,68,68,0.6);
        background: linear-gradient(135deg, #b91c1c 0%, #ef4444 100%);
    }
    
    /* Report Container */
    .stMarkdown {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🩺 AI Doctor Kiosk (Simulation)</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>An AI-powered emergency room triage simulation. <b>Strictly for educational purposes.</b></div>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
if not api_key:
    st.sidebar.warning("API Key needed for the AI Crew.")

# --- PATIENT INTAKE FORM ---
st.header("Patient Intake Form")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
with col2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

symptoms = st.text_area("Describe your symptoms in detail", placeholder="e.g., I woke up with a sharp pain in my lower right abdomen and feel nauseous.")
duration = st.selectbox("How long have you had these symptoms?", ["Less than 1 hour", "A few hours", "1-2 Days", "A week", "More than a week"])

if st.button("🚨 Run Diagnostic Triage", use_container_width=True):
    if not symptoms:
        st.error("Please describe your symptoms.")
    elif not api_key:
        st.error("Please provide a Gemini API key.")
    else:
        with st.spinner("The Triage Nurse, Safety Officer, and Diagnostician are reviewing your file..."):
            medical_report = run_medical_crew(age, gender, symptoms, duration, api_key)
            
            st.divider()
            st.markdown("### 📋 AI Diagnostic Report")
            st.markdown(medical_report)
            
st.markdown("---")
st.error("⚠️ **DISCLAIMER:** This application generates responses using Artificial Intelligence. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.")
