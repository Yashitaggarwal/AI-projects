# 🏦 AI Wealth Manager & Retirement Planner

An "Ultimate Agentic" financial planning tool that combines hard mathematical forecasting (Monte Carlo Simulations) with an autonomous team of AI experts (CrewAI) to evaluate your retirement readiness.

## Features
- **Monte Carlo Engine:** Uses `numpy` to run 1,000 simulations of market returns over your career, based on your risk profile, plotting the 10th, 50th, and 90th percentile trajectories.
- **CrewAI Financial Team:** 
  - **Tax Strategist:** Suggests tax-advantaged accounts and optimizations.
  - **CFP:** Translates the math into a holistic behavioral assessment of your retirement trajectory.
- **Beautiful UI:** Built with Streamlit and Plotly.

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
