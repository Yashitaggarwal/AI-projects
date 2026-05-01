from duckduckgo_search import DDGS
import google.generativeai as genai

def fetch_stock_news(ticker, max_results=5):
    """
    Fetches recent news headlines for a given stock ticker.
    """
    try:
        query = f"{ticker} stock news financial"
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []

def analyze_sentiment(news_items, api_key):
    """
    Uses Gemini to analyze the sentiment of a list of news items.
    """
    if not news_items:
        return "No news data available to analyze.", "Neutral"
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        news_text = "\n\n".join([f"Title: {item.get('title', '')}\nSnippet: {item.get('body', '')}" for item in news_items])
        
        prompt = f"""
        Analyze the sentiment of the following recent news headlines and snippets for a stock.
        
        News Data:
        {news_text}
        
        Task:
        1. Provide a brief summary of the overall news.
        2. Give an overall sentiment score: 'Bullish', 'Bearish', or 'Neutral'.
        3. Highlight any major risks or positive catalysts mentioned.
        
        Format as a short Markdown report. Start your report with a clear sentiment label on the first line, e.g., "Sentiment: Bullish".
        """
        
        response = model.generate_content(prompt)
        
        # Simple extraction for label
        sentiment_label = "Neutral"
        resp_lower = response.text.lower()
        if "sentiment: bullish" in resp_lower:
            sentiment_label = "Bullish"
        elif "sentiment: bearish" in resp_lower:
            sentiment_label = "Bearish"
            
        return response.text, sentiment_label
    except Exception as e:
        return f"Error analyzing sentiment: {e}", "Unknown"

def fetch_reddit_sentiment(ticker, max_results=5):
    """
    Fetches recent Reddit discussions from WallStreetBets or investing subs.
    """
    try:
        query = f"{ticker} site:reddit.com/r/wallstreetbets OR site:reddit.com/r/investing"
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        print(f"Error fetching Reddit sentiment for {ticker}: {e}")
        return []

def analyze_retail_sentiment(news_items, api_key):
    """
    Uses Gemini to specifically analyze retail sentiment (FOMO/Panic).
    """
    if not news_items:
        return "No retail discussions found.", "Neutral"
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        text = "\n\n".join([f"Title: {item.get('title', '')}\nPost: {item.get('body', '')}" for item in news_items])
        
        prompt = f"""
        Analyze the retail sentiment of the following Reddit discussions for a stock.
        
        Reddit Posts:
        {text}
        
        Task:
        1. Summarize the retail mood (e.g., FOMO, Panic, Squeezing, Holding).
        2. Give an overall retail sentiment score: 'Bullish', 'Bearish', or 'Neutral'.
        
        Format as a short Markdown report. Start your report with a clear sentiment label on the first line, e.g., "Retail Sentiment: Bullish".
        """
        
        response = model.generate_content(prompt)
        
        sentiment_label = "Neutral"
        resp_lower = response.text.lower()
        if "sentiment: bullish" in resp_lower:
            sentiment_label = "Bullish"
        elif "sentiment: bearish" in resp_lower:
            sentiment_label = "Bearish"
            
        return response.text, sentiment_label
    except Exception as e:
        return f"Error analyzing retail sentiment: {e}", "Unknown"
