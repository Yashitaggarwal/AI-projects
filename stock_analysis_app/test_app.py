import pandas as pd
from utils import fetch_stock_data, calculate_technical_indicators
from llm_analyst import configure_genai

def test_core_logic():
    print("Testing Data Fetching...")
    # Test with a reliable ticker
    df = fetch_stock_data("RELIANCE.NS", period="5d", interval="1d")
    if df.empty:
        print("[FAIL] Data fetching failed or returned empty.")
    else:
        print(f"[OK] Data fetched successfully. Shape: {df.shape}")
        
    print("\nTesting Technical Indicators...")
    df = calculate_technical_indicators(df)
    if 'RSI' in df.columns and 'MACD' in df.columns:
        print("[OK] Technical indicators calculated.")
    else:
        print("[FAIL] Technical indicators missing.")

    print("\nTesting LLM Configuration...")
    # Just test configuration, not actual generation without key
    if configure_genai("dummy_key"):
        print("[OK] Gemini configuration function works (logic only).")
    
if __name__ == "__main__":
    test_core_logic()
