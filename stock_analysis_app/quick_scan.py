import yfinance as yf
import ta
import pandas as pd

stocks = ['RELIANCE.NS', 'TATASTEEL.NS', 'INFY.NS', 'HDFCBANK.NS', 'TCS.NS', 'ICICIBANK.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS', 'AXISBANK.NS']

results = []
for ticker in stocks:
    try:
        df = yf.Ticker(ticker).history(period='1mo', interval='1d')
        if df.empty:
            continue
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        
        price = df['Close'].iloc[-1]
        rsi = df['RSI'].iloc[-1]
        macd_val = df['MACD'].iloc[-1]
        macd_sig = df['MACD_Signal'].iloc[-1]
        
        # Simple signal logic
        signal = 'HOLD'
        if rsi < 30 and macd_val > macd_sig:
            signal = 'STRONG BUY'
        elif rsi < 40 and macd_val > macd_sig:
            signal = 'BUY'
        elif rsi > 70 and macd_val < macd_sig:
            signal = 'SELL'
        elif rsi > 60 and macd_val < macd_sig:
            signal = 'WEAK SELL'
        elif macd_val > macd_sig:
            signal = 'BUY'
        elif macd_val < macd_sig:
            signal = 'SELL'
            
        results.append({
            'Ticker': ticker.replace('.NS',''), 
            'Price': round(price,2), 
            'RSI': round(rsi,2), 
            'MACD': round(macd_val,2), 
            'Signal': signal
        })
    except Exception as e:
        pass

df_results = pd.DataFrame(results)
print("=" * 60)
print("INDIAN STOCK MARKET ANALYSIS - TOP 10 STOCKS")
print("=" * 60)
print(df_results.to_string(index=False))
print()
print("=" * 60)
buy_stocks = df_results[df_results['Signal'].isin(['BUY', 'STRONG BUY'])]
if not buy_stocks.empty:
    print('RECOMMENDED TO BUY:')
    for _, row in buy_stocks.iterrows():
        ticker = row['Ticker']
        price = row['Price']
        rsi = row['RSI']
        signal = row['Signal']
        print(f"  -> {ticker} at Rs.{price} (RSI: {rsi}, Signal: {signal})")
else:
    print("No strong BUY signals at this time. Market may be overbought.")
print("=" * 60)
