import pandas as pd
import numpy as np
import plotly.graph_objects as go

def run_backtest(df, initial_capital=10000.0):
    """
    Simulates a simple MACD + RSI crossover strategy.
    Strategy: 
    Buy when MACD > Signal AND RSI < 40
    Sell when MACD < Signal OR RSI > 70
    """
    if df.empty or 'MACD' not in df.columns or 'RSI' not in df.columns:
        return None, None
        
    df = df.copy()
    
    # Initialize signals
    df['Signal'] = 0 
    
    # Generate Buy/Sell signals (1 = Buy, -1 = Sell, 0 = Hold)
    buy_condition = (df['MACD'] > df['MACD_Signal']) & (df['RSI'] < 40)
    sell_condition = (df['MACD'] < df['MACD_Signal']) | (df['RSI'] > 70)
    
    df.loc[buy_condition, 'Signal'] = 1
    df.loc[sell_condition, 'Signal'] = -1
    
    # Positions: 1 = Long, 0 = Flat
    # Forward fill positions based on signals
    df['Position'] = df['Signal'].replace(0, np.nan).ffill().fillna(0)
    # Map -1 back to 0 for flat position (we don't short in this basic model)
    df['Position'] = df['Position'].apply(lambda x: 1 if x == 1 else 0)
    
    # Shift position by 1 day to represent trading AT THE NEXT OPEN
    # Avoids lookahead bias
    df['Position'] = df['Position'].shift(1).fillna(0)
    
    # Calculate daily returns of the stock
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Calculate strategy returns (Position * Daily_Return)
    df['Strategy_Return'] = df['Position'] * df['Daily_Return']
    
    # Calculate cumulative returns
    df['Cumulative_Market'] = (1 + df['Daily_Return']).cumprod() * initial_capital
    df['Cumulative_Strategy'] = (1 + df['Strategy_Return']).cumprod() * initial_capital
    
    # Fill NAs in cumulative columns with initial capital
    df['Cumulative_Market'] = df['Cumulative_Market'].fillna(initial_capital)
    df['Cumulative_Strategy'] = df['Cumulative_Strategy'].fillna(initial_capital)
    
    # Metrics
    total_return_pct = (df['Cumulative_Strategy'].iloc[-1] / initial_capital - 1) * 100
    market_return_pct = (df['Cumulative_Market'].iloc[-1] / initial_capital - 1) * 100
    
    # Max Drawdown
    roll_max = df['Cumulative_Strategy'].cummax()
    drawdown = df['Cumulative_Strategy'] / roll_max - 1.0
    max_drawdown = drawdown.min() * 100
    
    metrics = {
        'Total Strategy Return (%)': round(total_return_pct, 2),
        'Buy & Hold Return (%)': round(market_return_pct, 2),
        'Max Drawdown (%)': round(max_drawdown, 2),
        'Final Equity': round(df['Cumulative_Strategy'].iloc[-1], 2)
    }
    
    return df, metrics

def plot_backtest(df, ticker):
    """Plots the equity curve of the strategy vs Buy & Hold."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df.index, y=df['Cumulative_Market'], name='Buy & Hold (Market)', line=dict(color='gray', dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Cumulative_Strategy'], name='AI Strategy (MACD+RSI)', line=dict(color='green', width=2)))
    
    fig.update_layout(
        title=f"AI Strategy Backtest vs Market for {ticker} (Initial $10k)",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        template="plotly_dark",
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig
