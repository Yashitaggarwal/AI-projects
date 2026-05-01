import numpy as np
import pandas as pd
import plotly.graph_objects as go

def run_monte_carlo(current_savings, annual_contribution, years, risk_profile="Moderate", simulations=1000):
    """
    Runs a Monte Carlo simulation for retirement forecasting.
    """
    # Define expected return (mu) and volatility (sigma) based on risk profile
    profiles = {
        "Conservative": {"mu": 0.04, "sigma": 0.05},
        "Moderate": {"mu": 0.07, "sigma": 0.12},
        "Aggressive": {"mu": 0.10, "sigma": 0.18}
    }
    
    mu = profiles.get(risk_profile, profiles["Moderate"])["mu"]
    sigma = profiles.get(risk_profile, profiles["Moderate"])["sigma"]
    
    # Initialize array to store all simulation paths
    portfolio_paths = np.zeros((simulations, years + 1))
    portfolio_paths[:, 0] = current_savings
    
    # Run simulations
    for i in range(simulations):
        for year in range(1, years + 1):
            # Calculate market return for this year (random normal distribution)
            annual_return = np.random.normal(mu, sigma)
            
            # Calculate new balance: previous balance * (1 + return) + annual contribution
            prev_balance = portfolio_paths[i, year - 1]
            new_balance = prev_balance * (1 + annual_return) + annual_contribution
            
            # Prevent portfolio from going below 0 in extreme cases
            portfolio_paths[i, year] = max(0, new_balance)
            
    # Calculate percentiles (10th, 50th/Median, 90th)
    percentile_10 = np.percentile(portfolio_paths, 10, axis=0)
    percentile_50 = np.percentile(portfolio_paths, 50, axis=0)
    percentile_90 = np.percentile(portfolio_paths, 90, axis=0)
    
    return {
        "paths": portfolio_paths,
        "p10": percentile_10,
        "p50": percentile_50,
        "p90": percentile_90,
        "final_median": percentile_50[-1],
        "final_p10": percentile_10[-1]
    }

def plot_monte_carlo(mc_results, years):
    """Generates a Plotly chart for the Monte Carlo results."""
    x_axis = list(range(years + 1))
    
    fig = go.Figure()
    
    # Plot 90th Percentile (Optimistic)
    fig.add_trace(go.Scatter(x=x_axis, y=mc_results['p90'], name='Optimistic (90th)', line=dict(color='rgba(0, 255, 0, 0.5)')))
    
    # Plot 10th Percentile (Pessimistic)
    fig.add_trace(go.Scatter(x=x_axis, y=mc_results['p10'], name='Pessimistic (10th)', line=dict(color='rgba(255, 0, 0, 0.5)'), fill='tonexty', fillcolor='rgba(128, 128, 128, 0.2)'))
    
    # Plot Median (Expected)
    fig.add_trace(go.Scatter(x=x_axis, y=mc_results['p50'], name='Expected (Median)', line=dict(color='white', width=3)))
    
    fig.update_layout(
        title="Retirement Wealth Projection (Monte Carlo Simulation)",
        xaxis_title="Years from Now",
        yaxis_title="Portfolio Value ($)",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig
