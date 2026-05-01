import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

def generate_forecast(df, periods=30):
    """
    Generates a price forecast using Prophet.
    Requires dataframe with datetime index and 'Close' column.
    """
    try:
        # Prepare data for Prophet
        prophet_df = df.reset_index()[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
        
        # Prophet requires timezone-naive datetime
        if pd.api.types.is_datetime64_any_dtype(prophet_df['ds']):
            if prophet_df['ds'].dt.tz is not None:
                prophet_df['ds'] = prophet_df['ds'].dt.tz_localize(None)

        model = Prophet(daily_seasonality=False, yearly_seasonality=True, weekly_seasonality=True)
        model.fit(prophet_df)
        
        future = model.make_future_dataframe(periods=periods)
        # Avoid timezone issues by localizing back if needed, but easier to keep naive
        forecast = model.predict(future)
        
        return forecast
    except Exception as e:
        print(f"Prophet forecasting failed: {e}")
        return None

def plot_forecast(forecast_df, original_df, ticker):
    """
    Creates a Plotly chart combining historical data and the forecast.
    """
    fig = go.Figure()
    
    # Original Data
    original_dates = original_df.index
    if original_dates.tz is not None:
         original_dates = original_dates.tz_localize(None)

    fig.add_trace(go.Scatter(x=original_dates, y=original_df['Close'], name='Historical Close', line=dict(color='cyan')))
    
    # Forecast
    fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat'], name='Predicted Trend', line=dict(color='orange', dash='dash')))
    
    # Confidence Interval
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_df['ds'], forecast_df['ds'][::-1]]),
        y=pd.concat([forecast_df['yhat_upper'], forecast_df['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Confidence Interval'
    ))
    
    fig.update_layout(
        title=f"AI Price Forecast for {ticker} (Prophet Model)", 
        xaxis_title="Date", 
        yaxis_title="Price",
        template="plotly_dark",
        height=500
    )
    return fig
