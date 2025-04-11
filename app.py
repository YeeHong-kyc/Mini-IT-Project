from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import qrcode
import os
from io import BytesIO
import base64
from models import db, User, Item, ScanHistory, SharedItem

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # In a real app, you'd get this from the logged-in user
    # For demo, we'll use user_id=1
    user_id = 1
    items = Item.query.filter_by(owner_id=user_id).all()
    shared_items = SharedItem.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', items=items, shared_items=shared_items)

@app.route('/item/new', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_id = 1  # From session in real app
        
        item = Item(name=name, description=description, owner_id=user_id)
        db.session.add(item)
        db.session.commit()
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"{request.host_url}scan/{item.id}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        qr_dir = os.path.join(app.static_folder, 'qrcodes')
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)
        qr_path = os.path.join(qr_dir, f'item_{item.id}.png')
        img.save(qr_path)
        
        item.qr_code_path = f'qrcodes/item_{item.id}.png'
        db.session.commit()
        
        flash('Item created successfully!', 'success')
        return redirect(url_for('view_item', item_id=item.id))
    
    return render_template('new_item.html')

@app.route('/item/<int:item_id>')
def view_item(item_id):
    item = Item.query.get_or_404(item_id)
    scans = ScanHistory.query.filter_by(item_id=item_id).order_by(ScanHistory.scan_time.desc()).all()
    return render_template('item.html', item=item, scans=scans)

@app.route('/scan/<int:item_id>')
def scan_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    # Record scan
    scan = ScanHistory(
        item_id=item.id,
        scan_time=datetime.now(),
        scanner_ip=request.remote_addr
    )
    db.session.add(scan)
    db.session.commit()
    
    return render_template('scan.html', item=item, scan=scan)

@app.route('/item/<int:item_id>/map')
def item_map(item_id):
    item = Item.query.get_or_404(item_id)
    scans = ScanHistory.query.filter_by(item_id=item_id).order_by(ScanHistory.scan_time.desc()).all()
    
    # Select MMU campus coordinates
    mmu_coords = {
        'lat': 3.0648,
        'lng': 101.6045,
        'zoom': 16
    }
    
    # Mock scan locations around MMU
    scan_locations = []
    for i, scan in enumerate(scans[:5]):  # Limit to 5 most recent
        scan_locations.append({
            'lat': mmu_coords['lat'] + (i * 0.0005),
            'lng': mmu_coords['lng'] + (i * 0.0005),
            'time': scan.scan_time.strftime('%Y-%m-%d %H:%M:%S'),
            'ip': scan.scanner_ip
        })
    
    return render_template('map.html', 
                         item=item, 
                         center=mmu_coords, 
                         locations=scan_locations)

@app.route('/item/<int:item_id>/share', methods=['GET', 'POST'])
def share_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('share_item', item_id=item_id))
        
        if SharedItem.query.filter_by(item_id=item_id, user_id=user.id).first():
            flash('Item is already shared with this user', 'warning')
            return redirect(url_for('share_item', item_id=item_id))
        
        shared_item = SharedItem(item_id=item_id, user_id=user.id)
        db.session.add(shared_item)
        db.session.commit()
        
        flash(f'Item shared successfully with {email}', 'success')
        return redirect(url_for('view_item', item_id=item_id))
    
    shared_with = db.session.query(User).join(SharedItem).filter(SharedItem.item_id == item_id).all()
    return render_template('share.html', item=item, shared_with=shared_with)

@app.route('/qrcodes/<path:filename>')
def serve_qrcode(filename):
    return send_from_directory(os.path.join(app.static_folder, 'qrcodes'), filename)

if __name__ == '__main__':
    app.run(debug=True)