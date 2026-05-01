# 🌍 Journezy Trip Planner - Streamlit Version

<div align="center">

![Journezy Trip Planner](https://img.shields.io/badge/Journezy-Trip%20Planner-orange?style=for-the-badge&logo=airplane)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red?style=for-the-badge&logo=streamlit)
![AI Powered](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-purple?style=for-the-badge&logo=google)

**Your Personal AI-Powered Travel Planning Assistant - Now with Streamlit!**

*Modern, interactive web interface for seamless travel planning*

</div>

---

## ✨ What's New in Streamlit Version

### 🎨 **Modern UI/UX**
- **Beautiful Interface**: Clean, modern design with gradient themes
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Interactive Widgets**: Intuitive form controls and real-time validation
- **Progress Tracking**: Visual feedback during trip planning
- **Tab-Based Navigation**: Organized content in easy-to-navigate tabs

### 🚀 **Enhanced Features**
- **Real-Time Updates**: Live progress indicators during planning
- **Chat Interface**: Interactive chat with travel assistant (coming soon)
- **Trip History**: Track your past trip plans (coming soon)
- **PDF Download**: Export your itinerary with one click
- **Session Management**: Persistent state across interactions
- **Smart Defaults**: Auto-fill based on traveler composition

### 💡 **Streamlit-Specific Features**
- **st.chat_message**: Modern chat interface
- **st.tabs**: Organized content sections
- **st.columns**: Responsive multi-column layouts
- **st.expander**: Collapsible sections for better organization
- **st.progress**: Visual progress tracking
- **st.balloons**: Celebration effects on success
- **st.download_button**: Easy PDF/markdown downloads
- **st.sidebar**: Configuration panel
- **st.metric**: Beautiful metric displays

---

## 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **Git** (for cloning the repository)

### Required API Keys
Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/saitej123/journezy-trip-planner.git
cd journezy-trip-planner-main
```

### 2. Install Dependencies

```bash
pip install -r requirements_streamlit.txt
```

### 3. Set Up Environment

Create a `.env` file with your API keys:

```bash
# Windows
notepad .env

# Mac/Linux
nano .env
```

Add the required API keys:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

### 4. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. **Configure Settings** (Sidebar)
- Select your preferred language (11 languages supported)
- Choose currency (USD or INR)
- Check API status

### 2. **Plan Your Trip** (Main Tab)

#### Basic Information
- **From City**: Enter departure city
- **To City**: Enter destination city
- **Dates**: Select start and end dates (future dates only)
- **Travelers**: Specify adults, children, seniors, and toddlers

#### Budget (Optional)
- Enter your total trip budget
- System will filter options within budget

#### Flight Preferences
- ✈️ **Avoid Red-Eye Flights**: Skip 10 PM - 6 AM flights
- 🌅 **Avoid Early Morning**: Skip flights before 8 AM
- 👶 **Child-Friendly Times**: Prefer 10 AM - 6 PM flights
- 👴 **Senior-Friendly Times**: Prefer 9 AM - 4 PM flights
- 🎯 **Direct Flights Only**: Show only non-stop flights

#### Special Considerations
- 👶 **Toddler-Friendly**: Include toddler-appropriate activities
- ♿ **Senior-Friendly**: Include accessible activities
- 🛡️ **Safety Check**: Include travel safety information

#### Additional Instructions
- Add any special requests or preferences
- Examples: dietary restrictions, interests, accessibility needs

### 3. **Generate Itinerary**
- Click "🚀 Generate Your Perfect Itinerary"
- Watch real-time progress updates
- View results in organized tabs

### 4. **Review Results**
- **📋 Itinerary**: Complete day-by-day plan
- **✈️ Flights**: Flight options with pricing
- **🏨 Hotels**: Accommodation recommendations
- **📍 Places**: Attractions and activities

### 5. **Download**
- Click "📥 Download Itinerary (PDF)" to save your plan
- Share with travel companions or keep for offline use

---

## 🎯 Key Features

### 🧠 **AI-Powered Intelligence**
- **Gemini 2.5 Flash**: Latest AI model for intelligent planning
- **Context-Aware**: Understands your preferences and constraints
- **Multi-Language**: Generate itineraries in 11 languages
- **Smart Recommendations**: Personalized suggestions based on traveler profile

### ✈️ **Comprehensive Travel Data**
- **Real-Time Flights**: Live pricing and availability via SerpAPI
- **Hotel Search**: Curated accommodations with ratings
- **Places Discovery**: Must-see attractions and hidden gems
- **Budget Management**: Filter options within your budget

### 👥 **Traveler-Centric**
- **Multi-Traveler Support**: Adults, children, seniors, toddlers
- **Smart Defaults**: Auto-select appropriate options
- **Accessibility**: Senior and toddler-friendly options
- **Flight Timing**: Optimized for different traveler types

### 📊 **Modern Interface**
- **Progress Tracking**: Visual feedback during planning
- **Tab Organization**: Easy navigation between sections
- **Responsive Design**: Works on all devices
- **Beautiful Styling**: Gradient themes and smooth animations

---

## 🏗️ Architecture

```
journezy-trip-planner-main/
├── 📄 streamlit_app.py          # Main Streamlit application
├── 📄 workflow.py                # Trip planning workflow
├── 📄 requirements_streamlit.txt # Streamlit dependencies
├── 📄 README_STREAMLIT.md        # This file
├── 📁 agents/                    # AI agents
│   ├── deligator.py             # Information extraction
│   └── itinerary_writer.py      # Itinerary generation
├── 📁 tools/                     # Search integrations
│   ├── flights.py               # Flight search
│   ├── hotels.py                # Hotel search
│   └── places.py                # Places search
└── 📁 utils/                     # Utility functions
    └── image_handler.py         # Image processing
```

---

## 🔧 Configuration

### Environment Variables

```env
# Required API Keys
GOOGLE_API_KEY=your_google_gemini_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

### Streamlit Configuration (Optional)

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

---

## 🚀 Advanced Features

### Session State Management
The app maintains state across interactions:
- Trip planning data
- Chat history
- Workflow status
- User preferences

### Async Processing
- Non-blocking trip planning
- Real-time progress updates
- Timeout handling (5 minutes)

### Error Handling
- Graceful error messages
- Fallback options
- Validation feedback

---

## 🎨 Customization

### Styling
Modify the CSS in `streamlit_app.py` to customize:
- Colors and gradients
- Button styles
- Card layouts
- Typography

### Features
Add new features by:
1. Creating new tabs
2. Adding widgets
3. Extending workflow
4. Integrating new APIs

---

## 📱 Responsive Design

The app is fully responsive and works on:
- 💻 **Desktop**: Full-featured experience
- 📱 **Tablet**: Optimized layout
- 📱 **Mobile**: Touch-friendly interface

---

## 🔒 Security

- API keys stored in `.env` file (not committed to git)
- Input validation on all forms
- Secure session management
- XSRF protection enabled

---

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements_streamlit.txt --force-reinstall
```

**2. API Key Issues**
```bash
# Check .env file exists and has correct keys
cat .env  # Mac/Linux
type .env  # Windows
```

**3. Port Already in Use**
```bash
# Run on different port
streamlit run streamlit_app.py --server.port 8502
```

**4. PDF Generation Fails**
```bash
# Install wkhtmltopdf (for pdfkit)
# Windows: Download from https://wkhtmltopdf.org/
# Mac: brew install wkhtmltopdf
# Linux: sudo apt-get install wkhtmltopdf
```

---

## 🆚 Streamlit vs FastAPI Version

| Feature | Streamlit | FastAPI |
|---------|-----------|---------|
| **Interface** | Interactive web app | REST API |
| **Deployment** | Single command | Requires web server |
| **User Experience** | Visual, interactive | Programmatic |
| **Real-time Updates** | Built-in | Requires WebSocket |
| **State Management** | Session state | External storage |
| **Best For** | End users | Developers/Integration |

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets (API keys)
4. Deploy!

### Docker
```bash
# Build image
docker build -t journezy-streamlit -f Dockerfile.streamlit .

# Run container
docker run -p 8501:8501 --env-file .env journezy-streamlit
```

### Heroku
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port=$PORT" > Procfile

# Deploy
heroku create journezy-trip-planner
git push heroku main
```

---

## 📊 Performance

- **Load Time**: < 2 seconds
- **Trip Planning**: 30-60 seconds (depends on API response)
- **Memory Usage**: ~200-300 MB
- **Concurrent Users**: Supports multiple sessions

---

## 🔮 Roadmap

### Coming Soon
- ✅ Interactive chat with AI assistant
- ✅ Trip history and saved plans
- ✅ Multi-destination trips
- ✅ Collaborative planning
- ✅ Calendar integration
- ✅ Weather forecasts
- ✅ Currency converter
- ✅ Expense tracking

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Streamlit**: For the amazing framework
- **Google Gemini**: For powerful AI capabilities
- **SerpAPI**: For real-time travel data
- **Community**: For feedback and contributions

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/saitej123/journezy-trip-planner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/saitej123/journezy-trip-planner/discussions)
- **Email**: support@journezy.com

---

<div align="center">

**Made with ❤️ and Streamlit for better travel planning**

[⬆ Back to Top](#-journezy-trip-planner---streamlit-version)

</div>
