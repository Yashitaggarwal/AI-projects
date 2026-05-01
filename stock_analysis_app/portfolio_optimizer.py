import numpy as np
import pandas as pd
import yfinance as yf
import scipy.optimize as sco
import plotly.graph_objects as go

def fetch_portfolio_data(tickers, period="2y"):
    """Fetches closing prices for a list of tickers."""
    data = {}
    for t in tickers:
        t = t.strip()
        if not t: continue
        try:
            df = yf.Ticker(t).history(period=period)
            if not df.empty:
                data[t] = df['Close']
        except Exception as e:
            print(f"Error fetching {t}: {e}")
            
    if not data:
        return pd.DataFrame()
        
    # Combine into single DataFrame and drop rows with NaN (incomplete data)
    portfolio_df = pd.DataFrame(data).dropna()
    return portfolio_df

def optimize_portfolio(df):
    """
    Calculates the Markowitz Efficient Frontier Tangency Portfolio (Max Sharpe).
    """
    if df.empty or len(df.columns) < 2:
        return None
        
    returns = df.pct_change().mean() * 252 # Annualized expected returns
    cov_matrix = df.pct_change().cov() * 252 # Annualized covariance matrix
    num_assets = len(df.columns)
    risk_free_rate = 0.05 # Assume 5% risk free rate 

    # Objective function: Minimize negative Sharpe Ratio
    def neg_sharpe_ratio(weights):
        p_ret = np.sum(returns * weights)
        p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        # Prevent division by zero
        if p_vol == 0: return 0 
        return -(p_ret - risk_free_rate) / p_vol

    # Constraints: sum of weights = 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # Bounds: weights between 0 and 1 (no short selling)
    bounds = tuple((0.0, 1.0) for _ in range(num_assets))
    # Initial guess: equal weighting
    init_guess = num_assets * [1. / num_assets]

    # Run optimization
    opt_results = sco.minimize(neg_sharpe_ratio, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Calculate final portfolio stats
    opt_weights = opt_results.x
    
    # Clean up weights (round very small numbers to 0)
    opt_weights = [round(w, 4) if w > 0.001 else 0.0 for w in opt_weights]
    
    opt_ret = np.sum(returns * opt_weights)
    opt_vol = np.sqrt(np.dot(np.array(opt_weights).T, np.dot(cov_matrix, opt_weights)))
    opt_sharpe = (opt_ret - risk_free_rate) / opt_vol if opt_vol > 0 else 0

    return {
        'weights': dict(zip(df.columns, opt_weights)),
        'return': opt_ret,
        'volatility': opt_vol,
        'sharpe': opt_sharpe
    }

def plot_portfolio_weights(weights_dict):
    """Creates a pie chart of the optimal portfolio allocation."""
    labels = list(weights_dict.keys())
    values = list(weights_dict.values())
    
    # Filter out 0% allocations for cleaner chart
    filtered_labels = [l for l, v in zip(labels, values) if v > 0]
    filtered_values = [v for v in values if v > 0]
    
    fig = go.Figure(data=[go.Pie(labels=filtered_labels, values=filtered_values, hole=.4, textinfo='label+percent')])
    fig.update_layout(
        title_text="Optimal Portfolio Allocation (Max Sharpe Ratio)", 
        template="plotly_dark",
        height=400,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    return fig
