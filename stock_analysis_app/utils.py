import yfinance as yf
import pandas as pd
import ta

def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetches historical stock data for the given ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def calculate_technical_indicators(df):
    """
    Calculates technical indicators: RSI, MACD, SMA, EMA, Bollinger Bands.
    """
    if df.empty:
        return df

    # RSI
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

    # MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Diff'] = macd.macd_diff()

    # SMA / EMA
    df['SMA_20'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
    df['EMA_20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    
    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
    df['BB_High'] = bollinger.bollinger_hband()
    df['BB_Low'] = bollinger.bollinger_lband()
    df['BB_Mid'] = bollinger.bollinger_mavg()

    # ADX
    adx = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], window=14)
    df['ADX'] = adx.adx()

    # Ichimoku Cloud
    ichimoku = ta.trend.IchimokuIndicator(df['High'], df['Low'], window1=9, window2=26, window3=52)
    df['Ichimoku_a'] = ichimoku.ichimoku_a()
    df['Ichimoku_b'] = ichimoku.ichimoku_b()

    return df

def get_latest_price(ticker):
    """
    Get the latest price and simple info.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    # yfinance info can be unreliable for real-time price on some international exchanges, 
    # so we might check the 'regularMarketPrice' or just use the last history row.
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    if not price:
        # Fallback to history
        hist = stock.history(period='1d')
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            
    return price, info
