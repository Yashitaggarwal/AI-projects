"""
City database for travel recommendations by country
"""

COUNTRY_CITIES = {
    "India": {
        "cities": ["Mumbai", "Delhi", "Bangalore", "Jaipur", "Goa", "Kerala", "Agra", "Varanasi", "Udaipur", "Rishikesh"],
        "popular": ["Mumbai", "Delhi", "Jaipur", "Goa", "Kerala"]
    },
    "USA": {
        "cities": ["New York", "Los Angeles", "San Francisco", "Las Vegas", "Miami", "Chicago", "Boston", "Seattle", "Orlando", "San Diego"],
        "popular": ["New York", "Los Angeles", "Las Vegas", "Miami", "San Francisco"]
    },
    "UK": {
        "cities": ["London", "Edinburgh", "Manchester", "Liverpool", "Oxford", "Cambridge", "Bath", "Brighton", "York", "Bristol"],
        "popular": ["London", "Edinburgh", "Manchester", "Oxford", "Bath"]
    },
    "France": {
        "cities": ["Paris", "Nice", "Lyon", "Marseille", "Bordeaux", "Strasbourg", "Toulouse", "Cannes", "Monaco", "Versailles"],
        "popular": ["Paris", "Nice", "Lyon", "Marseille", "Bordeaux"]
    },
    "Italy": {
        "cities": ["Rome", "Venice", "Florence", "Milan", "Naples", "Pisa", "Verona", "Bologna", "Turin", "Amalfi Coast"],
        "popular": ["Rome", "Venice", "Florence", "Milan", "Amalfi Coast"]
    },
    "Spain": {
        "cities": ["Barcelona", "Madrid", "Seville", "Valencia", "Granada", "Bilbao", "Malaga", "Toledo", "Ibiza", "San Sebastian"],
        "popular": ["Barcelona", "Madrid", "Seville", "Valencia", "Granada"]
    },
    "Japan": {
        "cities": ["Tokyo", "Kyoto", "Osaka", "Hiroshima", "Nara", "Yokohama", "Sapporo", "Fukuoka", "Nagoya", "Okinawa"],
        "popular": ["Tokyo", "Kyoto", "Osaka", "Hiroshima", "Nara"]
    },
    "Thailand": {
        "cities": ["Bangkok", "Phuket", "Chiang Mai", "Pattaya", "Krabi", "Koh Samui", "Ayutthaya", "Hua Hin", "Koh Phi Phi", "Chiang Rai"],
        "popular": ["Bangkok", "Phuket", "Chiang Mai", "Krabi", "Koh Samui"]
    },
    "Australia": {
        "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Cairns", "Hobart", "Darwin", "Canberra"],
        "popular": ["Sydney", "Melbourne", "Brisbane", "Cairns", "Gold Coast"]
    },
    "UAE": {
        "cities": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Al Ain"],
        "popular": ["Dubai", "Abu Dhabi", "Sharjah"]
    },
    "Switzerland": {
        "cities": ["Zurich", "Geneva", "Lucerne", "Interlaken", "Zermatt", "Bern", "Basel", "Lausanne", "Montreux", "St. Moritz"],
        "popular": ["Zurich", "Geneva", "Lucerne", "Interlaken", "Zermatt"]
    },
    "Greece": {
        "cities": ["Athens", "Santorini", "Mykonos", "Crete", "Rhodes", "Thessaloniki", "Corfu", "Zakynthos", "Delphi", "Meteora"],
        "popular": ["Athens", "Santorini", "Mykonos", "Crete", "Rhodes"]
    },
    "Turkey": {
        "cities": ["Istanbul", "Cappadocia", "Antalya", "Bodrum", "Izmir", "Ankara", "Pamukkale", "Ephesus", "Fethiye", "Marmaris"],
        "popular": ["Istanbul", "Cappadocia", "Antalya", "Bodrum", "Pamukkale"]
    },
    "Egypt": {
        "cities": ["Cairo", "Luxor", "Aswan", "Alexandria", "Hurghada", "Sharm El Sheikh", "Giza", "Dahab", "Marsa Alam"],
        "popular": ["Cairo", "Luxor", "Aswan", "Hurghada", "Sharm El Sheikh"]
    },
    "Brazil": {
        "cities": ["Rio de Janeiro", "São Paulo", "Salvador", "Brasília", "Florianópolis", "Fortaleza", "Manaus", "Recife", "Curitiba", "Porto Alegre"],
        "popular": ["Rio de Janeiro", "São Paulo", "Salvador", "Florianópolis", "Manaus"]
    },
    "Mexico": {
        "cities": ["Cancun", "Mexico City", "Playa del Carmen", "Tulum", "Puerto Vallarta", "Guadalajara", "Cabo San Lucas", "Oaxaca", "Merida", "Guanajuato"],
        "popular": ["Cancun", "Mexico City", "Playa del Carmen", "Tulum", "Puerto Vallarta"]
    },
    "Canada": {
        "cities": ["Toronto", "Vancouver", "Montreal", "Quebec City", "Calgary", "Ottawa", "Banff", "Victoria", "Niagara Falls", "Whistler"],
        "popular": ["Toronto", "Vancouver", "Montreal", "Quebec City", "Banff"]
    },
    "Germany": {
        "cities": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne", "Dresden", "Heidelberg", "Stuttgart", "Nuremberg", "Bremen"],
        "popular": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne"]
    },
    "Netherlands": {
        "cities": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", "Groningen", "Maastricht", "Delft", "Haarlem", "Leiden"],
        "popular": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Delft"]
    },
    "Portugal": {
        "cities": ["Lisbon", "Porto", "Algarve", "Sintra", "Coimbra", "Braga", "Évora", "Madeira", "Azores", "Cascais"],
        "popular": ["Lisbon", "Porto", "Algarve", "Sintra", "Madeira"]
    },
    "Indonesia": {
        "cities": ["Bali", "Jakarta", "Yogyakarta", "Lombok", "Bandung", "Surabaya", "Ubud", "Gili Islands", "Komodo", "Borobudur"],
        "popular": ["Bali", "Jakarta", "Yogyakarta", "Lombok", "Ubud"]
    },
    "Singapore": {
        "cities": ["Singapore City", "Sentosa", "Marina Bay", "Orchard Road", "Chinatown", "Little India", "Clarke Quay", "Jurong", "Changi"],
        "popular": ["Singapore City", "Sentosa", "Marina Bay"]
    },
    "Malaysia": {
        "cities": ["Kuala Lumpur", "Penang", "Langkawi", "Malacca", "Kota Kinabalu", "Johor Bahru", "Ipoh", "Cameron Highlands", "Perhentian Islands"],
        "popular": ["Kuala Lumpur", "Penang", "Langkawi", "Malacca", "Kota Kinabalu"]
    },
    "New Zealand": {
        "cities": ["Auckland", "Queenstown", "Wellington", "Christchurch", "Rotorua", "Dunedin", "Taupo", "Nelson", "Wanaka", "Milford Sound"],
        "popular": ["Auckland", "Queenstown", "Wellington", "Rotorua", "Milford Sound"]
    },
    "South Africa": {
        "cities": ["Cape Town", "Johannesburg", "Durban", "Kruger National Park", "Garden Route", "Stellenbosch", "Port Elizabeth", "Pretoria", "Knysna"],
        "popular": ["Cape Town", "Johannesburg", "Kruger National Park", "Garden Route", "Durban"]
    },
    "Morocco": {
        "cities": ["Marrakech", "Casablanca", "Fes", "Chefchaouen", "Rabat", "Tangier", "Essaouira", "Agadir", "Meknes", "Sahara Desert"],
        "popular": ["Marrakech", "Casablanca", "Fes", "Chefchaouen", "Sahara Desert"]
    },
    "Peru": {
        "cities": ["Lima", "Cusco", "Machu Picchu", "Arequipa", "Puno", "Nazca", "Iquitos", "Paracas", "Huaraz", "Sacred Valley"],
        "popular": ["Lima", "Cusco", "Machu Picchu", "Arequipa", "Sacred Valley"]
    },
    "Argentina": {
        "cities": ["Buenos Aires", "Mendoza", "Bariloche", "Ushuaia", "Salta", "Córdoba", "Iguazu Falls", "El Calafate", "Rosario", "Mar del Plata"],
        "popular": ["Buenos Aires", "Mendoza", "Bariloche", "Iguazu Falls", "Ushuaia"]
    }
}

def get_cities_for_country(country: str):
    """Get list of cities for a specific country"""
    return COUNTRY_CITIES.get(country, {}).get("cities", [])

def get_popular_cities_for_country(country: str):
    """Get popular cities for a specific country"""
    return COUNTRY_CITIES.get(country, {}).get("popular", [])

def get_city_recommendations(country: str, interests: list, limit: int = 3):
    """Get city recommendations based on country and interests"""
    cities = get_popular_cities_for_country(country)
    if not cities:
        cities = get_cities_for_country(country)
    
    return cities[:limit] if cities else []
