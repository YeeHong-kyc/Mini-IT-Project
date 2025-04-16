import sqlite3
from flask import Flask, render_template

def create_db():
    conn = sqlite3.connect('mmu.db')  
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print(" Database and 'users' table created successfully.")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('LoginInterface.html')

@app.route('/register')
def register():
    return render_template('Register.html')

@app.route('/confirm/')
def confirm():
    return render_template('confirmPassword.html')

if __name__ == '__main__':
    app.run(debug=True)

