# 🩺 AI Doctor Kiosk (Triage & Diagnosis)

An agentic medical simulation designed to mimic the workflow of an emergency room triage system.

## Features
- **Intake Nurse Agent:** Formats and categorizes the patient's reported symptoms.
- **Diagnostic Specialist:** Generates a Differential Diagnosis (top 3 potential conditions).
- **Safety Officer:** Screens the symptoms for "Red Flag" indicators (like chest pain or stroke symptoms) and recommends immediate ER visits if necessary.

> **DISCLAIMER:** This application is strictly for educational and simulation purposes. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Provide your Gemini API key in the `.env` file or directly in the sidebar.
2. Run the app:
```bash
streamlit run app.py
```
