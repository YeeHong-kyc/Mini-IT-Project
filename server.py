import sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_mmu_key_2025'

DB_PATH = 'mmu.db'

def create_db():
    conn = sqlite3.connect(DB_PATH)  
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
    print("Database and 'users' table created successfully.")


@app.route('/')
def home():
    return render_template('LoginInterface.html')
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[0], password):
        session['email'] = email  
        flash('Login successful!')
        return redirect(url_for('confirm'))  
    else:
        flash('Invalid email or password.')
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['psw-repeat']  

  
        if password != password_repeat:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

       
        hashed_pw = generate_password_hash(password)

    
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
            conn.commit()
            flash("Registration successful!")
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            flash("Email already registered.")
            return redirect(url_for('register'))
        finally:
            conn.close()

    return render_template('Register.html')

@app.route('/confirm/', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('confirm'))

        hashed_password = generate_password_hash(new_password)

        user_email = session['email']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, user_email))
        conn.commit()
        conn.close()

        flash("Password updated successfully.")
        return redirect(url_for('home'))

    return render_template('confirmPassword.html')

if __name__ == '__main__':
    create_db()
    app.run(debug=True)

