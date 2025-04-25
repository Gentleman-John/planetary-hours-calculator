import pytz
from astral import LocationInfo
from astral.sun import sun
from astral.geocoder import database, lookup
from datetime import datetime, timedelta

# Helper function to ensure datetimes are timezone-aware
def ensure_timezone_aware(dt):
    """Ensure datetime is timezone-aware by adding local timezone if needed."""
    if dt.tzinfo is None:
        # Get user's local timezone
        local_timezone = datetime.now().astimezone().tzinfo
        return dt.replace(tzinfo=local_timezone)
    return dt

# Planetary correspondences according to The Greater Key of Solomon
# Planetary rulership days (starting from Sunday)
WEEKDAY_PLANETS = {
    0: "Sun",     # Sunday
    1: "Moon",    # Monday
    2: "Mars",    # Tuesday
    3: "Mercury", # Wednesday
    4: "Jupiter", # Thursday
    5: "Venus",   # Friday
    6: "Saturn"   # Saturday
}

# Planetary hour sequence (Chaldean order)
PLANETARY_HOUR_SEQUENCE = [
    "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"
]

# Planet rulership data
PLANET_DATA = {
    "Sun": {
        "archangel": "Michael",
        "angel": "Dardiel",
        "color": "Gold",
        "metal": "Gold",
        "stone": "Yellow Diamond",
        "influence": "Power, success, leadership, vitality, confidence",
        "description": "The Sun represents light, life force, and divine authority. In Solomonic magic, it's associated with success and all matters of leadership and power."
    },
    "Moon": {
        "archangel": "Gabriel",
        "angel": "Neciel",
        "color": "Silver",
        "metal": "Silver",
        "stone": "Pearl, Moonstone",
        "influence": "Intuition, fertility, dreams, emotions, receptivity",
        "description": "The Moon governs intuition, dreams, and all things hidden or mysterious. It is tied to emotions, receptivity, and cycles of change."
    },
    "Mars": {
        "archangel": "Samael",
        "angel": "Madimiel",
        "color": "Red",
        "metal": "Iron",
        "stone": "Ruby",
        "influence": "Courage, strength, protection, overcoming enemies",
        "description": "Mars embodies strength, courage, and aggressive action. In Solomonic magic, Mars hours are ideal for protective work and overcoming obstacles."
    },
    "Mercury": {
        "archangel": "Raphael",
        "angel": "Cochabiel",
        "color": "Orange, Purple",
        "metal": "Mercury, Alloys",
        "stone": "Opal",
        "influence": "Communication, knowledge, travel, divination",
        "description": "Mercury governs communication, knowledge, and intellectual pursuits. These hours are excellent for divination, study, and uncovering hidden wisdom."
    },
    "Jupiter": {
        "archangel": "Tzadkiel",
        "angel": "Zedekel",
        "color": "Blue, Purple",
        "metal": "Tin",
        "stone": "Amethyst, Sapphire",
        "influence": "Prosperity, expansion, wisdom, legal matters",
        "description": "Jupiter represents growth, abundance, and wisdom. Jupiter hours are powerful for prosperity workings and expanding one's influence."
    },
    "Venus": {
        "archangel": "Anael",
        "angel": "Nogahiel",
        "color": "Green",
        "metal": "Copper",
        "stone": "Emerald",
        "influence": "Love, beauty, harmony, art, pleasure",
        "description": "Venus governs love, beauty, and harmony. In Solomonic tradition, Venus hours are ideal for works of art, love, and reconciliation."
    },
    "Saturn": {
        "archangel": "Cassiel",
        "angel": "Shabbathiel",
        "color": "Black, Dark Purple",
        "metal": "Lead",
        "stone": "Onyx, Obsidian",
        "influence": "Boundaries, discipline, banishing, binding",
        "description": "Saturn represents boundaries, time, and discipline. Saturn hours are powerful for binding, banishing, and ending situations."
    }
}

def calculate_sunrise_sunset(latitude, longitude, date=None):
    """Calculate sunrise and sunset times for a given location and date."""
    if date is None:
        date = datetime.now()
    
    # Create a location object
    location = LocationInfo(
        name="Custom Location",
        region="Region",
        timezone="UTC",
        latitude=latitude,
        longitude=longitude
    )
    
    # Get sun information for the location
    s = sun(location.observer, date=date, tzinfo=pytz.UTC)
    
    # Get user's local timezone
    local_timezone = datetime.now().astimezone().tzinfo
    
    # Convert to local timezone
    sunrise_local = s["sunrise"].astimezone(local_timezone)
    sunset_local = s["sunset"].astimezone(local_timezone)
    
    return sunrise_local, sunset_local

def get_planetary_hours(latitude, longitude, date=None):
    """Calculate all planetary hours for a given date and location."""
    if date is None:
        date = datetime.now()
    
    # Get sunrise and sunset times
    sunrise, sunset = calculate_sunrise_sunset(latitude, longitude, date)
    
    # Calculate day and night durations
    day_duration = (sunset - sunrise).total_seconds() / 3600  # in hours
    
    # Calculate next day's sunrise
    next_day = date + timedelta(days=1)
    next_sunrise, _ = calculate_sunrise_sunset(latitude, longitude, next_day)
    
    night_duration = (next_sunrise - sunset).total_seconds() / 3600  # in hours
    
    # Calculate the length of each planetary hour
    day_hour_length = day_duration / 12
    night_hour_length = night_duration / 12
    
    # Determine the ruling planet of the day (based on the weekday)
    day_of_week = date.weekday()  # 0 is Monday in Python
    day_of_week = (day_of_week + 1) % 7  # Convert to 0 = Sunday, 1 = Monday, etc.
    ruling_planet = WEEKDAY_PLANETS[day_of_week]
    
    # Find the position of the ruling planet in the sequence
    ruling_planet_index = PLANETARY_HOUR_SEQUENCE.index(ruling_planet)
    
    # Generate all hours for the day
    planetary_hours = []
    
    # Day hours (from sunrise to sunset)
    for i in range(12):
        start_time = sunrise + timedelta(hours=i * day_hour_length)
        end_time = sunrise + timedelta(hours=(i + 1) * day_hour_length)
        
        # Calculate the planet for this hour
        hour_index = (ruling_planet_index + i) % 7
        planet = PLANETARY_HOUR_SEQUENCE[hour_index]
        
        planetary_hours.append({
            "hour_number": i + 1,
            "period": "Day",
            "start_time": start_time,
            "end_time": end_time,
            "planet": planet,
            "archangel": PLANET_DATA[planet]["archangel"],
            "angel": PLANET_DATA[planet]["angel"],
            "duration": f"{day_hour_length:.2f} hours"
        })
    
    # Night hours (from sunset to next sunrise)
    for i in range(12):
        start_time = sunset + timedelta(hours=i * night_hour_length)
        end_time = sunset + timedelta(hours=(i + 1) * night_hour_length)
        
        # Calculate the planet for this hour
        hour_index = (ruling_planet_index + 12 + i) % 7
        planet = PLANETARY_HOUR_SEQUENCE[hour_index]
        
        planetary_hours.append({
            "hour_number": i + 1,
            "period": "Night",
            "start_time": start_time,
            "end_time": end_time,
            "planet": planet,
            "archangel": PLANET_DATA[planet]["archangel"],
            "angel": PLANET_DATA[planet]["angel"],
            "duration": f"{night_hour_length:.2f} hours"
        })
    
    return planetary_hours

def get_current_planetary_hour(latitude, longitude, current_time=None):
    """Determine the current planetary hour."""
    if current_time is None:
        current_time = datetime.now()
    
    # Ensure current_time is timezone-aware
    current_time = ensure_timezone_aware(current_time)
    
    # Get all planetary hours for the day
    hours = get_planetary_hours(latitude, longitude, current_time)
    
    # Find the current hour
    for hour in hours:
        # Ensure start_time and end_time are timezone-aware
        start_time = ensure_timezone_aware(hour["start_time"])
        end_time = ensure_timezone_aware(hour["end_time"])
        
        if start_time <= current_time < end_time:
            return hour
    
    # If not found (rare edge case), return the first hour of the day
    return hours[0]

def get_planetary_day_info(latitude, longitude, date=None):
    """Get information about the planetary day."""
    if date is None:
        date = datetime.now()
    
    # Determine the ruling planet of the day (based on the weekday)
    day_of_week = date.weekday()  # 0 is Monday in Python
    day_of_week = (day_of_week + 1) % 7  # Convert to 0 = Sunday, 1 = Monday, etc.
    ruling_planet = WEEKDAY_PLANETS[day_of_week]
    
    # Return information about the day
    return {
        "date": date.strftime("%A, %B %d, %Y"),
        "day_of_week": day_of_week,
        "planet": ruling_planet,
        "archangel": PLANET_DATA[ruling_planet]["archangel"],
        "angel": PLANET_DATA[ruling_planet]["angel"],
        "color": PLANET_DATA[ruling_planet]["color"],
        "metal": PLANET_DATA[ruling_planet]["metal"],
        "stone": PLANET_DATA[ruling_planet]["stone"],
        "influence": PLANET_DATA[ruling_planet]["influence"],
        "description": PLANET_DATA[ruling_planet]["description"]
    }

def get_current_planetary_hour_info(latitude, longitude, current_time=None):
    """Get detailed information about the current planetary hour."""
    if current_time is None:
        current_time = datetime.now()
    
    # Ensure current_time is timezone-aware
    current_time = ensure_timezone_aware(current_time)
    
    # Get current planetary hour
    hour = get_current_planetary_hour(latitude, longitude, current_time)
    planet = hour["planet"]
    
    # Add additional information
    hour.update({
        "color": PLANET_DATA[planet]["color"],
        "metal": PLANET_DATA[planet]["metal"],
        "stone": PLANET_DATA[planet]["stone"],
        "influence": PLANET_DATA[planet]["influence"],
        "description": PLANET_DATA[planet]["description"],
        "current_time": current_time.strftime("%H:%M:%S"),
        "progress": calculate_hour_progress(current_time, hour["start_time"], hour["end_time"])
    })
    
    return hour

def calculate_hour_progress(current_time, start_time, end_time):
    """Calculate the progress within the current planetary hour as a percentage."""
    # Ensure all datetime objects are timezone-aware
    current_time = ensure_timezone_aware(current_time)
    start_time = ensure_timezone_aware(start_time)
    end_time = ensure_timezone_aware(end_time)
        
    total_duration = (end_time - start_time).total_seconds()
    elapsed = (current_time - start_time).total_seconds()
    
    if total_duration <= 0:
        return 0
    
    progress = (elapsed / total_duration) * 100
    return min(max(0, progress), 100)  # Ensure it's between 0 and 100

def get_all_planetary_hours(latitude, longitude, date=None):
    """Get a complete list of all planetary hours for a day."""
    return get_planetary_hours(latitude, longitude, date)

def get_day_planetary_hours(latitude, longitude, date=None):
    """Format planetary hours for display with periods and time ranges."""
    hours = get_planetary_hours(latitude, longitude, date)
    
    # Format the hours for display
    day_hours = []
    
    # Create time-formatted version
    for hour in hours:
        day_hours.append({
            "hour_number": hour["hour_number"],
            "period": hour["period"],
            "time_range": f"{hour['start_time'].strftime('%H:%M')} - {hour['end_time'].strftime('%H:%M')}",
            "planet": hour["planet"],
            "archangel": hour["archangel"],
            "angel": hour["angel"],
            "start_time": hour["start_time"],
            "end_time": hour["end_time"]
        })
    
    return day_hours
