import google.generativeai as genai
import os

# ─────────────────────────────────────────────────────────────────────────────
# AGENTIC ANALYSIS MODULE
# Multi-agent stock analysis powered by Google Gemini.
# Simulates a financial research team: Technical Analyst, Fundamental Analyst,
# Risk Manager, and a Chief Investment Officer (CIO) for the final verdict.
# Uses sequential "agent handoff" — each agent builds on the previous.
# ─────────────────────────────────────────────────────────────────────────────

def _call_agent(model, role: str, context: str, question: str) -> str:
    """Helper to call an LLM agent with a specific persona."""
    prompt = f"""You are a {role}. {context}

Your specific task: {question}

Be concise, structured, and professional. Use markdown bullet points and bold headers."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"*Agent error: {e}*"


def run_agentic_analysis(
    ticker: str,
    current_price: float,
    technical_summary: str,
    news_summary: str,
    sentiment_label: str,
    api_key: str
) -> dict:
    """
    Runs a multi-agent analysis pipeline:
    1. Technical Analyst Agent
    2. Fundamental/News Analyst Agent
    3. Risk Manager Agent
    4. CIO (Chief Investment Officer) — final verdict
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    base_context = f"""
Stock Ticker: {ticker}
Current Price: {current_price}
Technical Indicators Summary:
{technical_summary}

Recent News Sentiment: {sentiment_label}
News Summary:
{news_summary}
"""

    # ── Agent 1: Technical Analyst ───────────────────────────────────────────
    tech_report = _call_agent(
        model,
        role="Senior Technical Analyst specializing in quantitative chart analysis",
        context=base_context,
        question=f"""
Analyze ONLY the technical indicators provided for {ticker}.
1. Interpret RSI, MACD, Bollinger Bands, SMA/EMA, ADX, and Ichimoku Cloud.
2. Identify key support and resistance levels (estimate based on indicators).
3. Identify any chart pattern signals (e.g., golden cross, death cross, BB squeeze).
4. State a technical bias: **Bullish**, **Bearish**, or **Neutral**, and explain why.
"""
    )

    # ── Agent 2: Fundamental / News Analyst ──────────────────────────────────
    fundamental_report = _call_agent(
        model,
        role="Senior Fundamental Analyst and Market Intelligence Expert",
        context=base_context + f"\n\nTechnical Analyst's Report:\n{tech_report}",
        question=f"""
Analyze the NEWS SENTIMENT and macroeconomic factors for {ticker}.
1. Summarize the key themes from the recent news.
2. Identify any material events (earnings, M&A, regulatory news, macro headwinds/tailwinds).
3. Assess whether the news sentiment ({sentiment_label}) SUPPORTS or CONTRADICTS the technical bias.
4. Provide a fundamental/news-driven bias: **Positive**, **Negative**, or **Mixed**.
"""
    )

    # ── Agent 3: Risk Manager ─────────────────────────────────────────────────
    risk_report = _call_agent(
        model,
        role="Chief Risk Officer (CRO) at a hedge fund",
        context=base_context + f"\n\nTechnical Report:\n{tech_report}\n\nFundamental Report:\n{fundamental_report}",
        question=f"""
Assess the risk profile for a potential trade in {ticker}.
1. Rate the overall risk level: **Low**, **Medium**, or **High**.
2. Identify the top 3 risks (technical, fundamental, and macro).
3. Suggest a reasonable stop-loss level based on the current price ({current_price}) and technical structure.
4. Suggest a risk/reward ratio and a potential target price for a 30-day horizon.
"""
    )

    # ── Agent 4: CIO — Final Verdict ─────────────────────────────────────────
    cio_verdict = _call_agent(
        model,
        role="Chief Investment Officer (CIO) of a top-tier investment fund",
        context=f"""
You have received reports from your research team for {ticker}.

--- TECHNICAL ANALYST REPORT ---
{tech_report}

--- FUNDAMENTAL ANALYST REPORT ---
{fundamental_report}

--- RISK MANAGER REPORT ---
{risk_report}
""",
        question=f"""
Synthesize all three reports and deliver the final investment verdict for {ticker}.
1. **Overall Assessment**: 1-2 sentences summarizing the stock's current situation.
2. **Recommendation**: One of: 🟢 STRONG BUY | 🟡 BUY | ⚪ HOLD | 🟠 SELL | 🔴 STRONG SELL
3. **Conviction Level**: Low / Medium / High (and why).
4. **Entry Strategy**: Ideal entry price range or conditions.
5. **Exit Targets**: Short-term (1-4 weeks) and medium-term (1-3 months) targets.
6. **Key Risks to Watch**: Top 2 risks that could invalidate this thesis.
7. **Disclaimer**: Always end with a one-line AI disclaimer.
"""
    )

    return {
        "technical_analyst": tech_report,
        "fundamental_analyst": fundamental_report,
        "risk_manager": risk_report,
        "cio_verdict": cio_verdict,
    }
