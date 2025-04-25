import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from planetary_hours import (
    get_planetary_day_info, 
    get_current_planetary_hour_info, 
    get_all_planetary_hours, 
    get_day_planetary_hours,
    calculate_sunrise_sunset
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "planetaryhourssecret")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the database with the app
db.init_app(app)

# Import models after initializing db
from models import Location, PlanetaryHourLog

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    """Render the main page with planetary hour information"""
    # Get location parameters from request or use default from database
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    
    # If no coordinates provided, try to get default from database
    if lat is None or lng is None:
        default_location = Location.query.filter_by(is_default=True).first()
        if default_location:
            lat = default_location.latitude
            lng = default_location.longitude
        else:
            # Use New York as fallback default if no saved default
            lat = 40.7128
            lng = -74.0060
    
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        lat = 40.7128
        lng = -74.0060
        
    # Get current planetary day and hour information
    day_info = get_planetary_day_info(lat, lng)
    hour_info = get_current_planetary_hour_info(lat, lng)
    
    # Get sunrise and sunset times
    sunrise, sunset = calculate_sunrise_sunset(lat, lng)
    
    # Get all planetary hours for the day
    all_hours = get_day_planetary_hours(lat, lng)
    
    return render_template(
        "index.html", 
        day_info=day_info, 
        hour_info=hour_info,
        all_hours=all_hours,
        sunrise=sunrise,
        sunset=sunset,
        lat=lat,
        lng=lng
    )

@app.route("/about")
def about():
    """Render the about page with information about planetary hours"""
    return render_template("about.html")

@app.route("/locations")
def list_locations():
    """View saved locations"""
    locations = Location.query.order_by(Location.name).all()
    return render_template("locations.html", locations=locations)

@app.route("/locations/add", methods=["GET", "POST"])
def add_location():
    """Add a new saved location"""
    if request.method == "POST":
        name = request.form.get("name")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        is_default = True if request.form.get("is_default") else False
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            flash("Please enter valid coordinates", "danger")
            return redirect(url_for("add_location"))
            
        # If this is the default, unset any existing defaults
        if is_default:
            default_locations = Location.query.filter_by(is_default=True).all()
            for loc in default_locations:
                loc.is_default = False
            
        location = Location(
            name=name,
            latitude=latitude,
            longitude=longitude,
            is_default=is_default
        )
        
        db.session.add(location)
        db.session.commit()
        
        flash(f"Location '{name}' has been added", "success")
        return redirect(url_for("list_locations"))
    
    # For GET requests, check if coordinates were provided in URL
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    
    try:
        lat = float(lat) if lat else None
        lng = float(lng) if lng else None
    except ValueError:
        lat = None
        lng = None
        
    return render_template("add_location.html", lat=lat, lng=lng)

@app.route("/locations/delete/<int:id>")
def delete_location(id):
    """Delete a saved location"""
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    
    flash(f"Location '{location.name}' has been deleted", "success")
    return redirect(url_for("list_locations"))

@app.route("/locations/use/<int:id>")
def use_location(id):
    """Use a saved location"""
    location = Location.query.get_or_404(id)
    return redirect(url_for("index", lat=location.latitude, lng=location.longitude))

@app.route("/log_query")
def log_query():
    """Log a planetary hour query"""
    lat = request.args.get("lat", "40.7128")
    lng = request.args.get("lng", "-74.0060")
    
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid coordinates"}), 400
    
    # Get current planetary hour information
    day_info = get_planetary_day_info(lat, lng)
    hour_info = get_current_planetary_hour_info(lat, lng)
    
    # Create log entry
    log = PlanetaryHourLog(
        latitude=lat,
        longitude=lng,
        day_planet=day_info["planet"],
        hour_planet=hour_info["planet"],
        period=hour_info["period"],
        hour_number=hour_info["hour_number"]
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"status": "success"})

@app.route("/api/planetary_hours")
def api_planetary_hours():
    """API endpoint to get planetary hour information"""
    lat = request.args.get("lat", "40.7128")
    lng = request.args.get("lng", "-74.0060")
    
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({"error": "Invalid coordinates"}), 400
    
    # Get current planetary day and hour information
    day_info = get_planetary_day_info(lat, lng)
    hour_info = get_current_planetary_hour_info(lat, lng)
    all_hours = get_all_planetary_hours(lat, lng)
    
    # Log this query in the database
    log = PlanetaryHourLog(
        latitude=lat,
        longitude=lng,
        day_planet=day_info["planet"],
        hour_planet=hour_info["planet"],
        period=hour_info["period"],
        hour_number=hour_info["hour_number"]
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        "day": day_info,
        "current_hour": hour_info,
        "all_hours": all_hours
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
