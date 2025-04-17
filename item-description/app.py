from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
print(f"Upload directory created at: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('itemdescription.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            image = request.files['image']

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                image.save(save_path)
                print(f"File saved to: {save_path}")

                new_item = Item(
                    title=title,
                    description=description,
                    image_filename=filename
                )
                db.session.add(new_item)
                db.session.commit()

                return render_template('result.html',
                                    title=title,
                                    description=description,
                                    image_url=f"uploads/{filename}")
            
            return "Invalid file type", 400
        
        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()
            return "An error occurred", 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)