from flask import Flask, request, render_template, jsonify
import sqlite3 as sql

app = Flask(__name__, static_url_path='/static')

# Create a function to check if a username already exists in the database
@app.route('/check_username', methods=['POST'])
def check_username(username):
    with sql.connect('logins.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM logins WHERE username=?", (username,))
        user = cur.fetchone()
        if user is None:
            # Username is available
            return True
        else:
            # Username is already taken
            return False

# Define the routes for your app
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/ingredients')
def ingredients():
    return render_template('ingredients.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

# Handle the registration form submission
@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    error = None

    if not firstname:
        error = 'First name is required.'
    elif not lastname:
        error = 'Last name is required.'
    elif not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif check_username(username) == False:
        error = 'Username already exists.'

    if error:
        return render_template('registration.html', error=error)
    
    # Insert the new user into the database
    with sql.connect('logins.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO logins (firstname, lastname, username, password) VALUES (?, ?, ?, ?)", (firstname, lastname, username, password))
        con.commit()
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)