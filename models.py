from app import db
from datetime import datetime

class Location(db.Model):
    """Model for storing user locations."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Location {self.name}: {self.latitude}, {self.longitude}>'
        
class PlanetaryHourLog(db.Model):
    """Model for logging planetary hour queries."""
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    day_planet = db.Column(db.String(20), nullable=False)
    hour_planet = db.Column(db.String(20), nullable=False)
    period = db.Column(db.String(10), nullable=False)  # 'Day' or 'Night'
    hour_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlanetaryHourLog {self.day_planet}/{self.hour_planet} at {self.timestamp}>'