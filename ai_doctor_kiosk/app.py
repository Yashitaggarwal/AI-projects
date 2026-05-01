import streamlit as st
import os
from dotenv import load_dotenv
from medical_crew import run_medical_crew

load_dotenv()

st.set_page_config(page_title="AI Doctor Kiosk", layout="centered", page_icon="🩺")

st.title("🩺 AI Doctor Kiosk (Simulation)")
st.markdown("An AI-powered emergency room triage simulation. **Strictly for educational purposes.**")

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
