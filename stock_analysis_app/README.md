# 📈 Global AI-Powered Stock Platform

An advanced, comprehensive stock market analysis application built with **Streamlit**. This platform goes far beyond basic charting by integrating a **Multi-Agent AI Framework**, **Machine Learning Price Forecasting**, and **Real-Time News Sentiment Analysis**. 

It is designed to give you institutional-grade insights into global equities (US, Indian markets, etc.) using the power of Google Gemini and open-source data.

---

## ✨ Key Features

### 🧠 True Autonomous Agents (`CrewAI`)
Powered by `CrewAI` and Google Gemini, the app simulates a full financial research team that actively browses the web for live data:
1. **Fundamental Analyst:** Autonomously searches for earnings, SEC filings, and macro catalysts.
2. **Risk Manager:** Scours the web for negative catalysts, regulatory risks, and competition.

### 🧪 AI Strategy Backtesting
Simulates trading an AI-driven technical strategy (MACD + RSI) over historical data. It plots the equity curve of the strategy versus a standard "Buy & Hold" approach, calculating metrics like Total Return and Max Drawdown.

### 🥧 Markowitz Portfolio Optimization
Input a basket of stocks (e.g., `AAPL, MSFT, TSLA, NVDA`) and the engine uses `scipy` math to calculate the **Tangency Portfolio**—the exact percentage allocation required to achieve the maximum Sharpe Ratio (highest return for lowest risk).

### 🦍 Alternative Data & Sentiment Scraping
Traditional news isn't enough. The app scrapes:
- **Wall Street News:** Institutional sentiment.
- **Reddit (r/WallStreetBets):** Measures "Retail FOMO", short squeeze chatter, and retail panic.

### 🔮 Machine Learning Forecasting
Integrates **Prophet** (Meta's open-source time-series forecasting tool) to project a 30-day predicted price trend, complete with confidence intervals, directly onto an interactive Plotly chart.

### 📊 Professional Interactive Dashboard
A beautiful, responsive Streamlit UI featuring:
- **Dark-mode** optimized layout.
- **Interactive Plotly Candlestick Charts** with toggleable technical overlays (Bollinger Bands, SMA, etc.).
- **Organized Tabs** separating Technicals, AI Reports, News feeds, and ML Forecasts.
- **Global Market Support:** Analyze US stocks (e.g., `AAPL`, `TSLA`) or Indian stocks (e.g., `RELIANCE.NS`).

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- A Google Gemini API Key (Get one free at [Google AI Studio](https://aistudio.google.com/))

### 1. Clone or Download the Repository
Navigate to the project directory:
```bash
cd stock_analysis_app
```

### 2. Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
You can either input your API key directly in the Streamlit UI sidebar, or create a `.env` file in the root directory for convenience:
```env
GEMINI_API_KEY=your_api_key_here
```

---

## 💻 Usage

Start the Streamlit application:
```bash
streamlit run main.py
```

1. Open your browser to the local address provided (usually `http://localhost:8501`).
2. Ensure your **Gemini API Key** is entered in the sidebar configuration.
3. Enter a **Stock Ticker**:
   - For US Stocks: `NVDA`, `AAPL`, `MSFT`
   - For Indian Stocks (NSE): `RELIANCE.NS`, `TCS.NS`
4. Select your desired time period and interval, then click **🚀 Analyze**.

> **Note:** The first time you run an analysis on a new ticker, it may take 10-15 seconds as the Prophet ML model trains and the AI agents generate their comprehensive reports. Subsequent chart interactions are instantaneous.

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Charting:** Plotly Graph Objects
- **Data Sourcing:** `yfinance`, `duckduckgo-search`
- **Machine Learning:** `prophet` (Time-Series Forecasting)
- **Technical Indicators:** `ta` (Technical Analysis Library)
- **Large Language Models:** Google Generative AI (`gemini-1.5-flash` / `gemini-pro`)

---

## ⚠️ Disclaimer
**For Educational Purposes Only.** This tool provides AI-driven analysis and machine learning forecasts. It does not constitute financial advice. Always consult with a certified financial advisor and do your own due diligence before making investment decisions. The stock market involves significant risk.
