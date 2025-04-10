# THIS IS A CONFIGURATION SETTINGS FOR THE SYSTEM.

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"  # For security session
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"  # Database file
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    QR_CODE_DIR = "static/qr_codes"  # Where QR codes are stored

# MMU Campus Coordinates (adjust to actual values)
MMU_BOUNDS = {  # Geo-fence coordinates
    "min_lat" : 3.0670,
    "max_lat" : 3.0699,
    "min_lng" : 101.6120,
    "max_lng" : 101.6170
}

# lat: latitude, lng: longitude