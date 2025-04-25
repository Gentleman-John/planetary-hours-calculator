# Planetary Hours Calculator

A Python web application that calculates planetary hours and their ruling entities according to The Greater Key of Solomon.

## Features

- Real-time calculation of current planetary hour and ruling planet
- Displays planetary correspondences including archangel, angel, and influences
- Location-based sunrise/sunset calculations for accurate planetary hour timing
- Interactive UI with dark theme and planetary icons
- Mobile-responsive design
- Save and manage favorite locations with PostgreSQL database
- Set default locations for automatic loading
- Track location and query history

## Technologies

- Flask web framework
- Astral library for astronomical calculations
- Bootstrap for responsive interface
- Custom JavaScript for dynamic content
- PostgreSQL database
- SQLAlchemy ORM

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/planetary-hours-calculator.git
cd planetary-hours-calculator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Configure the database:
```bash
# Create a PostgreSQL database
# Set environment variable for database connection
export DATABASE_URL=postgresql://username:password@localhost/planetary_hours
# Or add to a .env file
```

5. Run the application:
```bash
python main.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Usage

- The main page displays the current planetary hour information
- Use the location input fields to customize calculations for your specific location
- Click "Use My Location" to automatically detect your location (requires browser permission)
- The table shows all planetary hours for the current day
- Click "Save Location" to add your current coordinates to saved locations
- Access "My Locations" from the navigation menu to view, use, or delete saved locations
- Set a location as default to automatically load it when you open the application

## License

This project is open source and available under the [MIT License](LICENSE).