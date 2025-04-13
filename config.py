import os

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret key for session management, the 'your-secret-key-here' is just an example, can be changed
SECRET_KEY = 'your-secret-key-here'

# QR code settings
QR_CODE_DIR = os.path.join(basedir, 'static', 'qrcodes')