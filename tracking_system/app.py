from flask import Flask, render_template, request, jsonify, send_from_directory, current_app
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


# Routes
@app.route("/")
def home():
    return render_template("create_item.html")

@app.route("/create-item", methods = ["POST"])
def create_item():
    name = request.form["name"]
    description = request.form["description"]

    new_item = Item(name = name, description = description)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "item_id": new_item.id,
        "qr_code_url": f"/qrcode/{new_item.code}",
        "tracking_url": f"/track/{new_item.code}"
    })

@app.route("/track/<string:code>", methods = ["GET", "POST"])
def track_item(code):
    item = Item.query.filter_by(code = code).first_or_404()

    if request.method == "POST":
        # Handle location data from mobile devices
        lat = request.json.get("lat")
        lng = request.json.get("lng")

        if validate_location(lat, lng):
            new_scan = Scan(item_id = item.id, latitude = lat, longitude = lng)
            db.session.add(new_scan)
            db.session.commit()
            return jsonify({"status": "success"})
    
        return jsonify({"status": "error", "message": "Location outside campus"}), 400
    
    # For QR code scanning
    return render_template("track_item.html",
                           item = item,
                           scan_count = len(item.scans),
                           last_scan = item.scans[-1] if item.scans else None)

@app.route("/item/<string:code>")
def item_details(code):
    item = Item.query.filter_by(code = code).first_or_404()
    return render_template("item_details.html",
                           item = item,
                           scans = item.scans,
                           mmu_bounds = app.config["MMU_BOUNDS"])

@app.route("/qrcode/<string:code>")
def generate_qrcode(code):
    return send_from_directory(app.config["QR_CODE_DIR"], f"{code}.png")


#Helper Functions
def validate_location(lat, lng):
    bounds = app.config["MMU_BOUNDS"]
    try:
        lat = float(lat)
        lng = float(lng)
        return (bounds["min_lat"] <= lat <= bounds["max_lat"] and
                bounds["min_lng"] <= lng <= bounds["max_lng"])
    except ValueError:
        return False


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not os.path.exists(app.config["QR_CODE_DIR"]):
            os.makedirs(app.config["QR_CODE_DIR"])
    app.run(debug = True)


# This code is just sample
# To Be Modified...