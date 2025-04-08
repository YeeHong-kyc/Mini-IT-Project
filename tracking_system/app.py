from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from datetime import datetime
import uuid
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
QRcode(app)

# Database Models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)
    code = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    scans = db.relationship("Scan", backref = "item", lazy = True)

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable = False)
    scanned_at = db.Column(db.DateTime, default = datetime.utcnow)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)