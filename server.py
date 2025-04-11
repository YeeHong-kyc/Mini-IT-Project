from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('LoginInterface.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/confirm')
def confirm():
    return render_template('confirmPassword.html')

if __name__ == '__main__':
    app.run(debug=True)
    