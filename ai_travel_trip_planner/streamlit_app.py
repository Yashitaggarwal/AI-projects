"""
AI Travel Trip Planner — Ultimate Streamlit UI
Agno (7 agents) + CrewAI (4 agents) + Live Web Search
"""

import streamlit as st
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Travel Trip Planner", page_icon="✈️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(160deg, #060d20 0%, #0a1628 50%, #070f22 100%); color: #e2e8f0; }

.hero { background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(123,97,255,0.08));
  border: 1px solid rgba(0,212,255,0.18); border-radius: 20px; padding: 2.5rem 2rem;
  text-align: center; margin-bottom: 1.5rem; }
.hero h1 { font-size: 3rem !important; font-weight: 800 !important;
  background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #7b61ff 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { color: #94a3b8; font-size: 1.1rem; margin-top: 0.5rem; }
.badge { display: inline-block; background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3);
  border-radius: 20px; padding: 0.25rem 0.75rem; font-size: 0.8rem; color: #00d4ff; margin: 0.2rem; }

[data-testid="stSidebar"] { background: rgba(6,13,32,0.9) !important; backdrop-filter: blur(20px);
  border-right: 1px solid rgba(0,212,255,0.12); }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown { color: #cbd5e1 !important; }

h3 { color: #00d4ff !important; font-weight: 700 !important; font-size: 0.95rem !important;
  text-transform: uppercase; letter-spacing: 0.5px; padding-bottom: 0.3rem;
  border-bottom: 1px solid rgba(0,212,255,0.15); margin-top: 1.5rem !important; }

.stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea textarea {
  background: rgba(255,255,255,0.04) !important; color: #e2e8f0 !important;
  border: 1px solid rgba(0,212,255,0.2) !important; border-radius: 10px !important; }
.stTextInput>div>div>input:focus, .stTextArea textarea:focus {
  border-color: #00d4ff !important; box-shadow: 0 0 0 2px rgba(0,212,255,0.12) !important; }
.stSelectbox>div>div { background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(0,212,255,0.2) !important; border-radius: 10px !important; color: #e2e8f0 !important; }

.stButton>button { background: linear-gradient(135deg, #00d4ff, #0099ff, #7b61ff);
  color: #fff !important; font-weight: 700; border: none; padding: 0.85rem 2rem;
  border-radius: 12px; width: 100%; font-size: 1.05rem;
  box-shadow: 0 4px 20px rgba(0,212,255,0.35); transition: all 0.3s ease; }
.stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,212,255,0.55); }

[data-testid="metric-container"] { background: rgba(0,212,255,0.05);
  border: 1px solid rgba(0,212,255,0.18); border-radius: 14px; padding: 1rem;
  transition: transform 0.3s; }
[data-testid="metric-container"]:hover { transform: translateY(-4px); }
[data-testid="stMetricValue"] { color: #00d4ff !important; font-size: 1.8rem !important; font-weight: 700 !important; }

.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.02); border-radius: 12px;
  padding: 0.3rem; gap: 4px; border: 1px solid rgba(0,212,255,0.1); }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px;
  color: #64748b; font-weight: 600; border: none; transition: all 0.3s; }
.stTabs [data-baseweb="tab"]:hover { color: #00d4ff; background: rgba(0,212,255,0.06); }
.stTabs [aria-selected="true"] { background: rgba(0,212,255,0.15) !important;
  color: #00d4ff !important; border: 1px solid rgba(0,212,255,0.35) !important; }

.stProgress>div>div>div>div { background: linear-gradient(90deg, #00d4ff, #7b61ff); }
.stDownloadButton>button { background: linear-gradient(135deg, #10b981, #059669);
  color: white !important; box-shadow: 0 4px 15px rgba(16,185,129,0.3); }
hr { border-color: rgba(0,212,255,0.1) !important; }

.info-box { background: rgba(0,212,255,0.05); border: 1px solid rgba(0,212,255,0.15);
  border-radius: 12px; padding: 1.2rem; margin: 0.8rem 0; }
</style>
""", unsafe_allow_html=True)

from workflow import TourPlannerWorkflow
from main import TravelerInfo, FlightPreferences
from travel_crew import run_travel_crew

# Session state
for k, v in {"trip_data": None, "crew_result": None, "done": False, "from_city": "", "to_city": "", "start_date": None, "end_date": None, "days": 7, "currency": "USD", "budget": 0.0}.items():
    if k not in st.session_state:
        st.session_state[k] = v

async def run_agno(from_city, to_city, start_date, end_date, language, currency,
                   budget, travelers, fprefs, toddler, senior, safety, extra):
    try:
        q = f"Plan a comprehensive trip from {from_city} to {to_city} from {start_date} to {end_date}."
        if extra: q += f" {extra}"
        if travelers.adults: q += f" {travelers.adults} adult(s)"
        if travelers.children: q += f", {travelers.children} child(ren)"
        if travelers.seniors: q += f", {travelers.seniors} senior(s)"
        if travelers.children_under_5: q += f", {travelers.children_under_5} toddler(s)"
        wf = TourPlannerWorkflow(language=language)
        result = await wf.run(query=q, budget_amount=budget, currency=currency,
                              travelers=travelers, flight_preferences=fprefs,
                              consider_toddler_friendly=toddler,
                              consider_senior_friendly=senior, safety_check=safety)
        return {"status": "success", "result": result, "workflow": wf}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def main():
    # Hero
    st.markdown("""
    <div class="hero">
      <h1>✈️ AI Travel Trip Planner</h1>
      <p>The world's most comprehensive agentic travel intelligence platform</p>
      <div style="margin-top:1rem">
        <span class="badge">🤖 Agno 7-Agent Team</span>
        <span class="badge">🧠 CrewAI 4-Agent Crew</span>
        <span class="badge">🌐 Live Web Search</span>
        <span class="badge">🚂 All Transport Modes</span>
        <span class="badge">💎 Gemini 1.5 Pro</span>
        <span class="badge">🌍 Every Destination</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        api_key = st.text_input("🔑 Gemini API Key", type="password",
            value=os.getenv("GEMINI_API_KEY","") or os.getenv("GOOGLE_API_KEY",""))
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
            os.environ["GOOGLE_API_KEY"] = api_key

        st.markdown("---")
        lang_map = {"English":"en","Hindi":"hi","Spanish":"es","French":"fr","German":"de",
                    "Japanese":"ja","Korean":"ko","Arabic":"ar","Portuguese":"pt","Italian":"it"}
        lang_sel = st.selectbox("🌐 Itinerary Language", list(lang_map.keys()))
        language = lang_map[lang_sel]
        currency = st.selectbox("💰 Currency", ["USD","INR","EUR","GBP","AED","JPY","AUD","CAD","SGD"])

        st.markdown("---")
        with st.expander("🤖 How It Works"):
            st.markdown("""
**Agno Team (7 Agents):**
- 🚂 Travel Access & Routes
- 🏨 Accommodation Scout
- 🚌 Ground Transport
- 🛂 Visa & Culture Intel
- 🍜 Food & Experiences
- ☀️ Weather & Packing
- 📋 Itinerary Director

**CrewAI Crew (4 Agents):**
- 💰 Budget Analyst
- 💎 Hidden Gems Scout
- 🔧 Local Fixer
- 📅 Itinerary Synthesizer

All agents do **live internet search**.
            """)
        status = "✅" if (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")) else "❌ Missing"
        st.markdown(f"**API:** {status}")

    # Form
    st.markdown("### 🌍 Where Do You Want To Go?")
    c1, c2 = st.columns(2)
    with c1:
        from_city = st.text_input("📍 Departing From", placeholder="e.g., Mumbai, London, Tokyo")
        start_date = st.date_input("🗓️ Departure Date", value=datetime.now().date(), min_value=datetime.now().date())
        adults = st.number_input("👨 Adults", 1, 20, 1)
        seniors = st.number_input("👴 Seniors (65+)", 0, 20, 0)
    with c2:
        to_city = st.text_input("📍 Destination", placeholder="e.g., Santorini, Bhutan, Antarctica")
        end_date = st.date_input("🗓️ Return Date", value=(datetime.now()+timedelta(days=7)).date(), min_value=datetime.now().date())
        children = st.number_input("👦 Children (5-17)", 0, 20, 0)
        toddlers = st.number_input("👶 Toddlers (<5)", 0, 10, 0)

    st.markdown("### 💰 Budget & Preferences")
    bc1, bc2 = st.columns([3,1])
    with bc1:
        budget = st.number_input(f"Total Budget ({currency})", 0.0, step=500.0, value=0.0,
                                  help="Leave 0 for flexible — agents will give options at all price levels")
    with bc2:
        st.metric("Currency", currency)

    st.markdown("### 🚂 Getting There — Preferences")
    p1, p2, p3 = st.columns(3)
    with p1:
        avoid_red_eye = st.checkbox("🌙 Avoid Night Travel")
        child_times = st.checkbox("👶 Child-Friendly Times", value=(children>0 or toddlers>0))
    with p2:
        avoid_early = st.checkbox("🌅 Avoid Early Morning")
        senior_times = st.checkbox("👴 Senior-Friendly Times", value=seniors>0)
    with p3:
        direct_only = st.checkbox("🎯 Non-Stop / Direct Only")

    st.markdown("### 🎨 Special Requirements")
    s1, s2, s3 = st.columns(3)
    with s1: toddler_ok = st.checkbox("🧸 Toddler-Friendly", value=toddlers>0)
    with s2: senior_ok = st.checkbox("♿ Senior-Accessible", value=seniors>0)
    with s3: safety = st.checkbox("🛡️ Safety Assessment", value=True)

    extra = st.text_area("📝 Special Requests / Interests",
        placeholder="e.g., Vegetarian food, adventure sports, honeymoon, wheelchair access, museum lover, backpacker budget...",
        height=80)

    st.markdown("---")
    mode = st.radio("🤖 Planning Mode", 
        ["🚀 Full Power (Agno + CrewAI)", "⚡ Agno Team Only", "🕵️ CrewAI Local Deep-Dive"],
        horizontal=True)

    if st.button("✈️ Generate My Ultimate Travel Plan", use_container_width=True):
        if not from_city or not to_city:
            st.error("Please enter both departure and destination."); st.stop()
        if from_city.lower().strip() == to_city.lower().strip():
            st.error("Departure and destination can't be the same."); st.stop()
        if end_date < start_date:
            st.error("Return date must be after departure."); st.stop()
        if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
            st.error("Please add your Gemini API key in the sidebar."); st.stop()

        days = max(1, (end_date - start_date).days)
        st.session_state.from_city = from_city
        st.session_state.to_city = to_city
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.session_state.days = days
        st.session_state.currency = currency
        st.session_state.budget = budget

        travelers = TravelerInfo(adults=adults, children=children, seniors=seniors, children_under_5=toddlers)
        fprefs = FlightPreferences(avoid_red_eye=avoid_red_eye, avoid_early_morning=avoid_early,
                                   child_friendly=child_times, senior_friendly=senior_times,
                                   direct_flights_only=direct_only)
        ak = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        # Metrics
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("📅 Duration", f"{days} days")
        m2.metric("👥 Travelers", adults+children+seniors+toddlers)
        m3.metric("💰 Budget", f"{budget:,.0f} {currency}" if budget>0 else "Flexible")
        m4.metric("🌍 Route", f"{from_city[:8]} → {to_city[:8]}")

        if mode in ["🚀 Full Power (Agno + CrewAI)", "⚡ Agno Team Only"]:
            with st.spinner("🤖 7-Agent Agno team researching every detail of your trip..."):
                prog = st.progress(0); msg = st.empty()
                stages = ["🔍 Researching transport options...", "🏨 Scouting accommodation...",
                          "🚌 Mapping ground transport...", "🛂 Checking visa & culture...",
                          "🍜 Finding best food & experiences...", "☀️ Analysing weather & packing...",
                          "📋 Compiling master itinerary..."]
                try:
                    import threading
                    for i, s in enumerate(stages):
                        msg.text(s); prog.progress(int((i+1)/len(stages)*80))
                    result = asyncio.run(run_agno(from_city, to_city,
                        start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"),
                        language, currency, budget if budget>0 else None,
                        travelers, fprefs, toddler_ok, senior_ok, safety, extra))
                    prog.progress(100); msg.empty(); prog.empty()
                    if result["status"] == "success":
                        st.session_state.trip_data = result
                        st.session_state.done = True
                    else:
                        st.error(f"Agno error: {result.get('error')}")
                except Exception as e:
                    msg.empty(); prog.empty()
                    st.error(f"Agno team error: {e}")

        if mode in ["🚀 Full Power (Agno + CrewAI)", "🕵️ CrewAI Local Deep-Dive"]:
            with st.spinner("🕵️ CrewAI crew finding hidden gems, budget breakdowns & local secrets..."):
                try:
                    crew_r = run_travel_crew(to_city, days, f"{budget} {currency}", ak)
                    st.session_state.crew_result = crew_r
                    st.session_state.done = True
                except Exception as e:
                    st.warning(f"CrewAI crew issue: {e}")

        if st.session_state.done:
            st.success("✅ Your AI travel plan is ready! Scroll down to explore.")
            st.balloons()

    # Results
    if st.session_state.done:
        st.markdown("---")
        st.markdown("## 🎉 Your Comprehensive AI Travel Plan")
        st.markdown(f"**{st.session_state.from_city} → {st.session_state.to_city} · {st.session_state.days} days · {st.session_state.currency}**")

        tabs = st.tabs([
            "🗺️ Full Itinerary",
            "🕵️ Hidden Gems & Local Tips",
            "📊 Trip Summary",
        ])

        with tabs[0]:
            st.markdown("### 🗺️ AI Master Itinerary")
            st.caption("Generated by Agno 7-Agent Team with live internet research")
            if st.session_state.trip_data and st.session_state.trip_data.get("status") == "success":
                wf = st.session_state.trip_data.get("workflow")
                content = ""
                if wf and hasattr(wf, "itinerary") and wf.itinerary:
                    content = str(wf.itinerary)
                elif st.session_state.trip_data.get("result"):
                    content = str(st.session_state.trip_data["result"])
                if content:
                    st.markdown(content)
                    st.download_button("📥 Download Itinerary (.md)", data=content,
                        file_name=f"itinerary_{st.session_state.to_city}_{st.session_state.start_date}.md",
                        mime="text/markdown", use_container_width=True)
                else:
                    st.info("Agno team ran. If empty, try re-running or check API key.")
            else:
                st.info("Run with Agno Team to see the master itinerary here.")

        with tabs[1]:
            st.markdown("### 🕵️ CrewAI Local Intelligence Report")
            st.caption("Budget breakdown · Hidden gems · Practical tips · Local fixer insights")
            if st.session_state.crew_result:
                st.markdown(st.session_state.crew_result)
                st.download_button("📥 Download Local Guide (.md)",
                    data=st.session_state.crew_result,
                    file_name=f"local_guide_{st.session_state.to_city}.md",
                    mime="text/markdown", use_container_width=True)
            else:
                st.info("Select Full Power or CrewAI mode to get local deep-dive intelligence.")

        with tabs[2]:
            st.markdown("### 📊 Trip Summary")
            fc = st.session_state.from_city
            tc = st.session_state.to_city
            sd = st.session_state.start_date
            ed = st.session_state.end_date
            days = st.session_state.days
            cur = st.session_state.currency
            bud = st.session_state.budget
            st.markdown(f"""
| Field | Value |
|---|---|
| 🛫 From | `{fc}` |
| 🛬 To | `{tc}` |
| 📅 Dates | `{sd}` → `{ed}` |
| 🗓️ Duration | `{days} days` |
| 👥 Travelers | Adults: {adults} · Children: {children} · Seniors: {seniors} · Toddlers: {toddlers} |
| 💰 Budget | {f"{bud:,.0f} {cur}" if bud > 0 else "Flexible"} |
| 🌐 Language | {lang_sel} |
| 🛡️ Safety Assessment | {'Yes' if safety else 'No'} |
| 🤖 Mode | {mode} |
            """)

    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#334155;font-size:0.82rem'>⚡ Powered by Agno · CrewAI · Google Gemini · LangChain · DuckDuckGo Live Search</p>",
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()
