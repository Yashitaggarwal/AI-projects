"""
Journezy Trip Planner - Streamlit Version
AI-powered travel planning with real-time data
"""

import streamlit as st
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import base64
from typing import Optional
import sys

# Load environment variables
load_dotenv()

# Import workflow and tools
from workflow import TourPlannerWorkflow
from main import TravelerInfo, FlightPreferences

# Use Gemini API directly for inspiration
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Journezy Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for EaseMyTrip-inspired styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
        background-color: #f5f7fa;
    }
    
    /* Header styling - Blue gradient like EaseMyTrip */
    .header-container {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Button styling - Orange accent like EaseMyTrip */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(255, 107, 53, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4);
        background: linear-gradient(135deg, #FF8C42 0%, #FF6B35 100%);
    }
    
    /* Tab styling - Blue theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background: #f5f7fa;
        border-radius: 8px;
        font-weight: 600;
        color: #333;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e3f2fd;
        border-color: #2196F3;
        color: #1976D2;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%) !important;
        color: white !important;
        border-color: #1976D2 !important;
        box-shadow: 0 4px 10px rgba(33, 150, 243, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #e0e0e0;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #2196F3;
    }
    
    /* Success/Info boxes */
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        border-radius: 8px;
    }
    
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border-left: 4px solid #FF6B35;
        border-radius: 8px;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1976D2;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        color: white;
        box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
    }
    
    /* Sidebar styling - Blue gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2196F3 0%, #1976D2 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stDateInput>div>div>input:focus {
        border-color: #2196F3;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        display: flex;
        align-items: flex-start;
    }
    
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    
    .assistant-message {
        background: #fff3e0;
        border-left: 4px solid #FF6B35;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2196F3 0%, #1976D2 100%);
    }
    
    /* Checkbox styling */
    .stCheckbox {
        color: #333;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: #2196F3;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'trip_data' not in st.session_state:
        st.session_state.trip_data = None
    if 'planning_complete' not in st.session_state:
        st.session_state.planning_complete = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'workflow_status' not in st.session_state:
        st.session_state.workflow_status = []
    if 'trip_phase' not in st.session_state:
        st.session_state.trip_phase = 'inspiration'
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'interests': [],
            'past_destinations': [],
            'travel_style': 'balanced',
            'budget_preference': 'moderate'
        }
    if 'current_trip' not in st.session_state:
        st.session_state.current_trip = None
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
    if 'recommended_destinations' not in st.session_state:
        st.session_state.recommended_destinations = []
    if 'packing_list' not in st.session_state:
        st.session_state.packing_list = {}

initialize_session_state()

def add_chat_message(role: str, content: str):
    """Add a message to chat history"""
    st.session_state.chat_history.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now()
    })

def display_chat_history():
    """Display chat history"""
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

def update_workflow_status(status: str):
    """Update workflow status"""
    st.session_state.workflow_status.append({
        'status': status,
        'timestamp': datetime.now()
    })

async def plan_trip_async(
    from_city: str,
    to_city: str,
    start_date: str,
    end_date: str,
    language: str,
    currency: str,
    budget_amount: Optional[float],
    travelers: TravelerInfo,
    flight_preferences: FlightPreferences,
    consider_toddler_friendly: bool,
    consider_senior_friendly: bool,
    safety_check: bool,
    additional_instructions: str
):
    """Async function to plan trip"""
    try:
        # Build query
        query = f"Plan a trip from {from_city} to {to_city} from {start_date} to {end_date}."
        
        if additional_instructions:
            query += f" {additional_instructions}"
        
        # Add traveler context
        if travelers.adults > 0:
            query += f" Traveling with {travelers.adults} adult(s)"
        if travelers.children > 0:
            query += f", {travelers.children} child(ren)"
        if travelers.seniors > 0:
            query += f", {travelers.seniors} senior(s)"
        if travelers.children_under_5 > 0:
            query += f", {travelers.children_under_5} toddler(s)"
        
        # Create workflow
        workflow = TourPlannerWorkflow(language=language)
        
        # Run workflow
        result = await workflow.run(
            query=query,
            budget_amount=budget_amount,
            currency=currency,
            travelers=travelers,
            flight_preferences=flight_preferences,
            consider_toddler_friendly=consider_toddler_friendly,
            consider_senior_friendly=consider_senior_friendly,
            safety_check=safety_check
        )
        
        return {
            'status': 'success',
            'result': result,
            'workflow': workflow
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="header-title">✈️ Journezy Trip Planner</div>
        <div class="header-subtitle">AI-Powered Travel Planning</div>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Language selection
        language_options = {
            'English': 'en',
            'Hindi': 'hi',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Chinese': 'zh',
            'Arabic': 'ar'
        }
        selected_language = st.selectbox(
            "🌐 Language",
            options=list(language_options.keys()),
            index=0,
            help="Select the language for your itinerary"
        )
        language = language_options[selected_language]
        
        # Currency selection
        currency = st.selectbox(
            "💰 Currency",
            options=['USD', 'INR'],
            index=0,
            help="Select your preferred currency"
        )
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
            **Journezy Trip Planner** uses advanced AI to create personalized travel itineraries.
            
            **Features:**
            - 🤖 AI-powered Trip Planning
            - ✈️ Real-time flight search
            - 🏨 Hotel recommendations
            - 📍 Places to visit
            - 🗺️ Day-by-day itineraries
            - 📄 PDF export
            
            **Version:** 2.0 (Streamlit)
            """)
        
        # API Status
        with st.expander("🔑 API Status", expanded=False):
            google_api = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
            serpapi_key = os.getenv('SERPAPI_KEY')
            
            st.markdown(f"""
            - Google API: {'✅ Configured' if google_api else '❌ Missing'}
            - SerpAPI: {'✅ Configured' if serpapi_key else '❌ Missing'}
            """)
    
    # Main content area
    with st.container():
        # PLAN TRIP TAB (PRIMARY)
        st.markdown("### 🗺️ Plan Your Perfect Trip")
        
        col1, col2 = st.columns(2)
        
        with col1:
            from_city = st.text_input(
                "📍 From City",
                placeholder="e.g., New York, London, Tokyo",
                help="Enter your departure city"
            )
            
            start_date = st.date_input(
                "📅 Start Date",
                value=datetime.now().date(),
                min_value=datetime.now().date(),
                help="Select your departure date"
            )
            
            adults = st.number_input(
                "👨 Adults",
                min_value=1,
                max_value=10,
                value=1,
                help="Number of adults (18+)"
            )
            
            seniors = st.number_input(
                "👴 Seniors",
                min_value=0,
                max_value=10,
                value=0,
                help="Number of seniors (65+)"
            )
        
        with col2:
            to_city = st.text_input(
                "📍 To City",
                placeholder="e.g., Paris, Dubai, Singapore",
                help="Enter your destination city"
            )
            
            end_date = st.date_input(
                "📅 End Date",
                value=(datetime.now() + timedelta(days=7)).date(),
                min_value=datetime.now().date(),
                help="Select your return date"
            )
            
            children = st.number_input(
                "👦 Children (5-17)",
                min_value=0,
                max_value=10,
                value=0,
                help="Number of children aged 5-17"
            )
            
            children_under_5 = st.number_input(
                "👶 Toddlers (Under 5)",
                min_value=0,
                max_value=10,
                value=0,
                help="Number of children under 5"
            )
        
        # Budget section
        st.markdown("### 💵 Budget (Optional)")
        col1, col2 = st.columns([3, 1])
        with col1:
            budget_amount = st.number_input(
                f"Budget Amount ({currency})",
                min_value=0.0,
                value=0.0,
                step=100.0,
                help="Enter your total trip budget (optional)"
            )
        with col2:
            st.metric("Currency", currency)
        
        # Flight preferences
        st.markdown("### ✈️ Flight Preferences")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avoid_red_eye = st.checkbox(
                "🌙 Avoid Red-Eye Flights",
                help="Avoid flights between 10 PM - 6 AM"
            )
            child_friendly = st.checkbox(
                "👶 Child-Friendly Times",
                value=children > 0 or children_under_5 > 0,
                help="Prefer flights between 10 AM - 6 PM"
            )
        
        with col2:
            avoid_early_morning = st.checkbox(
                "🌅 Avoid Early Morning",
                help="Avoid flights before 8 AM"
            )
            senior_friendly = st.checkbox(
                "👴 Senior-Friendly Times",
                value=seniors > 0,
                help="Prefer flights between 9 AM - 4 PM"
            )
        
        with col3:
            direct_flights_only = st.checkbox(
                "🎯 Direct Flights Only",
                help="Show only non-stop flights"
            )
        
        # Special considerations
        st.markdown("### 🎨 Special Considerations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            consider_toddler_friendly = st.checkbox(
                "👶 Toddler-Friendly",
                value=children_under_5 > 0,
                help="Include toddler-friendly activities"
            )
        
        with col2:
            consider_senior_friendly = st.checkbox(
                "♿ Senior-Friendly",
                value=seniors > 0,
                help="Include accessible activities"
            )
        
        with col3:
            safety_check = st.checkbox(
                "🛡️ Safety Check",
                value=True,
                help="Include travel safety information"
            )
        
        # Additional instructions
        st.markdown("### 📝 Additional Instructions (Optional)")
        additional_instructions = st.text_area(
            "Any special requests or preferences?",
            placeholder="e.g., I prefer vegetarian restaurants, interested in historical sites, need wheelchair accessibility...",
            height=100
        )
        
        # Generate button
        st.markdown("---")
        
        if st.button("🚀 Generate Your Perfect Itinerary", type="primary", width='stretch'):
            # Validation
            if not from_city or not to_city:
                st.error("❌ Please enter both departure and destination cities")
            elif from_city.lower().strip() == to_city.lower().strip():
                st.error("❌ Departure and destination cities cannot be the same")
            elif end_date < start_date:
                st.error("❌ End date must be after start date")
            else:
                # Create traveler info
                travelers = TravelerInfo(
                    adults=adults,
                    children=children,
                    seniors=seniors,
                    children_under_5=children_under_5
                )
                
                # Create flight preferences
                flight_preferences = FlightPreferences(
                    avoid_red_eye=avoid_red_eye,
                    avoid_early_morning=avoid_early_morning,
                    child_friendly=child_friendly,
                    senior_friendly=senior_friendly,
                    direct_flights_only=direct_flights_only
                )
                
                # Show progress
                with st.spinner("🤖 Planning your perfect trip with AI..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Update progress
                    status_text.text("🔍 Analyzing your requirements...")
                    progress_bar.progress(20)
                    
                    # Run async workflow
                    try:
                        result = asyncio.run(plan_trip_async(
                            from_city=from_city,
                            to_city=to_city,
                            start_date=start_date.strftime("%Y-%m-%d"),
                            end_date=end_date.strftime("%Y-%m-%d"),
                            language=language,
                            currency=currency,
                            budget_amount=budget_amount if budget_amount > 0 else None,
                            travelers=travelers,
                            flight_preferences=flight_preferences,
                            consider_toddler_friendly=consider_toddler_friendly,
                            consider_senior_friendly=consider_senior_friendly,
                            safety_check=safety_check,
                            additional_instructions=additional_instructions
                        ))
                        
                        status_text.text("✈️ Finding best flights...")
                        progress_bar.progress(40)
                        
                        status_text.text("🏨 Searching for hotels...")
                        progress_bar.progress(60)
                        
                        status_text.text("📍 Discovering places to visit...")
                        progress_bar.progress(80)
                        
                        status_text.text("📝 Generating your itinerary...")
                        progress_bar.progress(100)
                        
                        if result['status'] == 'success':
                            st.session_state.trip_data = result
                            st.session_state.planning_complete = True
                            
                            status_text.empty()
                            progress_bar.empty()
                            
                            st.success("✅ Your trip has been planned successfully!")
                            st.balloons()
                            
                            # Add to chat history
                            add_chat_message('user', f"Plan a trip from {from_city} to {to_city}")
                            add_chat_message('assistant', "I've created a comprehensive travel plan for you!")
                            
                        else:
                            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                            
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        progress_bar.empty()
                        status_text.empty()
        
        # Display results if available
        if st.session_state.planning_complete and st.session_state.trip_data:
            st.markdown("---")
            st.markdown("## 🎉 Your Trip Plan")
            
            result = st.session_state.trip_data
            workflow = result.get('workflow')
            
            # Create tabs for different sections
            result_tabs = st.tabs(["📋 Itinerary", "✈️ Flights", "🏨 Hotels", "📍 Places"])
            
            with result_tabs[0]:
                st.markdown("### 📋 Complete Itinerary")
                if workflow and hasattr(workflow, 'itinerary'):
                    st.markdown(workflow.itinerary)
                    
                    # Download button for PDF
                    if isinstance(result['result'], str) and len(result['result']) > 1000:
                        try:
                            pdf_data = base64.b64decode(result['result'])
                            st.download_button(
                                label="📥 Download Itinerary (PDF)",
                                data=pdf_data,
                                file_name=f"itinerary_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                width='stretch'
                            )
                        except:
                            st.download_button(
                                label="📥 Download Itinerary (Text)",
                                data=workflow.itinerary,
                                file_name=f"itinerary_{datetime.now().strftime('%Y%m%d')}.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                else:
                    st.info("No itinerary data available")
            
            with result_tabs[1]:
                st.markdown("### ✈️ Flight Options")
                if workflow and hasattr(workflow, 'flights_data') and workflow.flights_data:
                    st.text(workflow.flights_data)
                else:
                    st.info("No flight data available")
            
            with result_tabs[2]:
                st.markdown("### 🏨 Hotel Recommendations")
                if workflow and hasattr(workflow, 'hotels_data') and workflow.hotels_data:
                    st.text(workflow.hotels_data)
                else:
                    st.info("No hotel data available")
            
            with result_tabs[3]:
                st.markdown("### 📍 Places to Visit")
                if workflow and hasattr(workflow, 'places_data') and workflow.places_data:
                    st.text(workflow.places_data)
                else:
                    st.info("No places data available")

if __name__ == "__main__":
    main()
