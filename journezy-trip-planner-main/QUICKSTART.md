# 🚀 Quick Start Guide - Journezy Trip Planner (Streamlit)

Get up and running with Journezy Trip Planner in 5 minutes!

---

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **pip** (Python package manager)
- ✅ **Google API Key** (for Gemini AI)
- ✅ **SerpAPI Key** (for flight/hotel search)

---

## ⚡ Installation Steps

### Step 1: Get API Keys

#### Google API Key (Gemini)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

#### SerpAPI Key
1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for a free account
3. Copy your API key from the dashboard

### Step 2: Clone or Download

```bash
# If you have git
git clone https://github.com/saitej123/journezy-trip-planner.git
cd journezy-trip-planner-main

# Or download and extract the ZIP file
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements_streamlit.txt
```

### Step 4: Configure API Keys

Create a `.env` file in the project root:

**Windows:**
```bash
notepad .env
```

**Mac/Linux:**
```bash
nano .env
```

Add your API keys:
```env
GOOGLE_API_KEY=your_google_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

Save and close the file.

### Step 5: Run the App

**Windows:**
```bash
# Double-click run_streamlit.bat
# OR run in terminal:
streamlit run streamlit_app.py
```

**Mac/Linux:**
```bash
streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🎯 First Trip Planning

### 1. Fill in Basic Information
- **From City**: e.g., "New York"
- **To City**: e.g., "Paris"
- **Start Date**: Select your departure date
- **End Date**: Select your return date
- **Travelers**: Number of adults, children, seniors, toddlers

### 2. Set Your Budget (Optional)
- Enter total trip budget in USD or INR
- System will filter options within budget

### 3. Configure Flight Preferences
- ✈️ Avoid red-eye flights (10 PM - 6 AM)
- 🌅 Avoid early morning flights (before 8 AM)
- 👶 Child-friendly times (10 AM - 6 PM)
- 👴 Senior-friendly times (9 AM - 4 PM)
- 🎯 Direct flights only

### 4. Special Considerations
- 👶 Toddler-friendly activities
- ♿ Senior-friendly options
- 🛡️ Safety check

### 5. Generate Itinerary
Click "🚀 Generate Your Perfect Itinerary" and wait 30-60 seconds

### 6. Review & Download
- View your complete itinerary
- Check flights, hotels, and places
- Download as PDF

---

## 🎨 Customization

### Change Language
Use the sidebar to select from 11 languages:
- English, Hindi, Spanish, French, German
- Italian, Portuguese, Japanese, Korean
- Chinese, Arabic

### Change Currency
Switch between USD and INR in the sidebar

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements_streamlit.txt --force-reinstall
```

### "API Key not found" Error
1. Check `.env` file exists in project root
2. Verify API keys are correct
3. No quotes around API keys in `.env`

### Port Already in Use
```bash
streamlit run streamlit_app.py --server.port 8502
```

### PDF Generation Fails
Install wkhtmltopdf:
- **Windows**: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/)
- **Mac**: `brew install wkhtmltopdf`
- **Linux**: `sudo apt-get install wkhtmltopdf`

---

## 💡 Tips for Best Results

### 1. Be Specific
- Use full city names: "New York City" not "NYC"
- Include country if ambiguous: "Paris, France"

### 2. Realistic Dates
- Plan at least 1 week in advance
- Allow 3-7 days for best results

### 3. Budget Planning
- Include flights, hotels, food, activities
- Add 20% buffer for unexpected costs

### 4. Traveler Information
- Accurate count helps with recommendations
- Enable special options for better results

### 5. Additional Instructions
Use this field for:
- Dietary restrictions
- Mobility requirements
- Special interests
- Activity preferences

---

## 📊 Example Queries

### Family Trip
```
From: Los Angeles
To: Orlando
Dates: Next month, 7 days
Travelers: 2 adults, 2 children
Budget: $5000 USD
Preferences: Child-friendly, theme parks
```

### Romantic Getaway
```
From: London
To: Venice
Dates: Next month, 4 days
Travelers: 2 adults
Budget: €2000
Preferences: Romantic restaurants, gondola rides
```

### Senior Travel
```
From: Toronto
To: Victoria
Dates: Next month, 5 days
Travelers: 2 seniors
Preferences: Senior-friendly, accessible, gardens
```

---

## 🔄 Updating the App

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements_streamlit.txt --upgrade

# Restart the app
streamlit run streamlit_app.py
```

---

## 📱 Mobile Access

The app works on mobile devices:
1. Run the app on your computer
2. Find your local IP address
3. Access from mobile: `http://YOUR_IP:8501`

**Find your IP:**
- **Windows**: `ipconfig`
- **Mac/Linux**: `ifconfig` or `ip addr`

---

## 🆘 Getting Help

### Check API Status
Look in the sidebar under "🔑 API Status" to verify your keys are configured.

### Common Issues

**Slow Response?**
- SerpAPI has rate limits on free tier
- Gemini API may be slow during peak hours
- Try again in a few minutes

**No Flights Found?**
- Check city names are correct
- Try different dates
- Disable "Direct flights only"

**No Hotels Found?**
- Verify destination city name
- Check dates are valid
- Try nearby cities

---

## 🎓 Learning Resources

### Streamlit Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

### API Documentation
- [Google Gemini API](https://ai.google.dev/docs)
- [SerpAPI Docs](https://serpapi.com/docs)

---

## ✅ Success Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] `.env` file created with valid API keys
- [ ] No firewall blocking port 8501
- [ ] Internet connection active
- [ ] API keys have remaining quota

---

## 🎉 You're Ready!

You now have everything you need to start planning amazing trips with AI!

**Next Steps:**
1. Plan your first trip
2. Explore different destinations
3. Try various preferences
4. Share with friends and family

---

## 📞 Support

- **Documentation**: See [README_STREAMLIT.md](README_STREAMLIT.md)
- **Issues**: [GitHub Issues](https://github.com/saitej123/journezy-trip-planner/issues)
- **Questions**: [GitHub Discussions](https://github.com/saitej123/journezy-trip-planner/discussions)

---

<div align="center">

**Happy Travels! ✈️🌍**

Made with ❤️ using Streamlit and Gemini AI

</div>
