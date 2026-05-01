import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# --- Local Modules ---
from utils import fetch_stock_data, calculate_technical_indicators
from sentiment_scraper import fetch_stock_news, analyze_sentiment, fetch_reddit_sentiment, analyze_retail_sentiment
from ml_forecasting import generate_forecast, plot_forecast
from agentic_analysis import run_agentic_analysis
from backtester import run_backtest, plot_backtest
from portfolio_optimizer import fetch_portfolio_data, optimize_portfolio, plot_portfolio_weights
from advanced_crew import run_crewai_analysis

load_dotenv()

st.set_page_config(page_title="Global AI Stock Platform (Enterprise)", layout="wide", page_icon="📈")

st.title("📈 Enterprise AI Stock Platform")
st.markdown("Advanced Tools: Agentic LLMs, Backtesting, MPT Optimization, and Alternative Data.")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))

if not api_key:
    st.sidebar.warning("API Key needed for AI features.")

# Navigation Mode
app_mode = st.sidebar.radio("Select Tool Mode", ["Single Stock Analysis", "Portfolio Optimizer"])

# --- MODE 1: SINGLE STOCK ---
if app_mode == "Single Stock Analysis":
    ticker_input = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", value="AAPL").upper()
    period = st.sidebar.selectbox("Period", ["6mo", "1y", "2y", "5y"], index=1)
    
    if st.sidebar.button("🚀 Analyze Ticker", use_container_width=True):
        with st.spinner(f"Fetching data for {ticker_input}..."):
            df = fetch_stock_data(ticker_input, period)
            if df.empty:
                st.error("No data found. Check ticker.")
                st.stop()
                
            df = calculate_technical_indicators(df)
            current_price = df['Close'].iloc[-1]
            
            # Create Tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Technicals", "🧪 Strategy Backtest", "🤖 CrewAI Analysts", "📰 News & Sentiment", "🔮 Forecast"])

            # --- TAB 1: TECHNICALS ---
            with tab1:
                st.metric("Current Price", f"${current_price:.2f}")
                fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
                fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)

            # --- TAB 2: BACKTESTING ---
            with tab2:
                st.subheader("MACD + RSI Strategy Backtest")
                st.markdown("Simulating historical performance if an AI traded this specific technical strategy vs Buy & Hold.")
                bt_df, metrics = run_backtest(df)
                if bt_df is not None:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Strategy Return", f"{metrics['Total Strategy Return (%)']}%")
                    col2.metric("Market Return", f"{metrics['Buy & Hold Return (%)']}%")
                    col3.metric("Max Drawdown", f"{metrics['Max Drawdown (%)']}%")
                    
                    bt_fig = plot_backtest(bt_df, ticker_input)
                    st.plotly_chart(bt_fig, use_container_width=True)
                else:
                    st.warning("Not enough data to run backtest.")

            # --- TAB 3: CREW AI ---
            with tab3:
                st.subheader("Autonomous Tool-Using Agents (CrewAI)")
                st.markdown("Warning: This uses live web-searching agents and may take 30-60 seconds.")
                if api_key:
                    if st.button("Trigger Autonomous Crew"):
                        with st.spinner("Agents are searching the web and conferring..."):
                            crew_result = run_crewai_analysis(ticker_input, api_key)
                            st.markdown("### Crew Final Report")
                            st.info(crew_result)
                else:
                    st.error("API Key required.")

            # --- TAB 4: SENTIMENT & REDDIT ---
            with tab4:
                colA, colB = st.columns(2)
                with colA:
                    st.subheader("Wall Street News")
                    news = fetch_stock_news(ticker_input)
                    if api_key:
                        summary, sent = analyze_sentiment(news, api_key)
                        st.metric("Institutional Sentiment", sent)
                        st.write(summary)
                with colB:
                    st.subheader("Retail FOMO (Reddit)")
                    reddit = fetch_reddit_sentiment(ticker_input)
                    if api_key:
                        r_summary, r_sent = analyze_retail_sentiment(reddit, api_key)
                        st.metric("Retail Sentiment", r_sent)
                        st.write(r_summary)

            # --- TAB 5: FORECAST ---
            with tab5:
                st.subheader("Prophet ML Forecast")
                forecast_df = generate_forecast(df, periods=30)
                if forecast_df is not None:
                    forecast_fig = plot_forecast(forecast_df, df, ticker_input)
                    st.plotly_chart(forecast_fig, use_container_width=True)

# --- MODE 2: PORTFOLIO OPTIMIZER ---
elif app_mode == "Portfolio Optimizer":
    st.header("🥧 Markowitz Portfolio Optimizer")
    st.markdown("Enter a basket of stocks to find the mathematically optimal allocation (Max Sharpe Ratio).")
    
    tickers_str = st.sidebar.text_input("Tickers (comma separated)", "AAPL, MSFT, TSLA, NVDA, GOOG")
    
    if st.button("Optimize Portfolio"):
        ticker_list = [x.strip().upper() for x in tickers_str.split(",")]
        with st.spinner("Downloading matrix data and optimizing..."):
            port_df = fetch_portfolio_data(ticker_list)
            if port_df.empty or len(port_df.columns) < 2:
                st.error("Need at least 2 valid tickers to optimize.")
            else:
                results = optimize_portfolio(port_df)
                if results:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Expected Annual Return", f"{results['return']*100:.2f}%")
                    col2.metric("Annual Volatility (Risk)", f"{results['volatility']*100:.2f}%")
                    col3.metric("Sharpe Ratio", f"{results['sharpe']:.2f}")
                    
                    fig = plot_portfolio_weights(results['weights'])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Optimization failed.")
