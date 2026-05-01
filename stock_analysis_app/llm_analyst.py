import google.generativeai as genai
import os

def configure_genai(api_key):
    """
    Configures the Gemini API with the provided key.
    """
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return False

def analyze_stock(ticker, current_price, data_summary, technical_summary):
    """
    Generates an analysis using Gemini Pro.
    """
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    You are a professional financial analyst. Analyze the following Indian stock data for {ticker}.
    
    **Current Market Data:**
    - Current Price: ₹{current_price}
    
    **Technical Indicators:**
    {technical_summary}
    
    **Recent Data Summary (Last 5 days):**
    {data_summary}
    
    **Task:**
    1. Analyze the technical indicators (RSI, MACD, Moving Averages, Bollinger Bands).
    2. Identify any bullish or bearish signals.
    3. Assess the risk level (Low, Medium, High).
    4. Provide a recommendation: BUY, SELL, or HOLD, with a clear rationale.
    5. Suggest a potential target price and stop-loss level based on the technicals (Disclaimer: Educational purpose only).
    
    **Constraint:**
    - Be concise and structured. 
    - Use bullet points.
    - Explicitly state that this is AI-generated analysis and not financial advice.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating analysis: {e}"
