from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
from passlib.hash import sha256_crypt
from flask import g

app = Flask(__name__, static_url_path='/static')

currUser = None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect('tb.db', check_same_thread=False)
    return db

# Close the database connection at the end of each request
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create a function to check if a username already exists in the database
@app.route('/check_username', methods=['POST'])
def check_username(username):
    with get_db() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM logins WHERE username=?", (username,))
        user = cur.fetchone()
        if user is None:
            # Username is available
            return True
        else:
            # Username is already taken
            return False

# Define the routes for the app
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/favorites')
def favorites():
    conn = sql.connect('tb.db')
    c = conn.cursor()
    c.execute("SELECT favorites FROM favs where login_id = ?;", (currUser,))
    names = c.fetchall()
    conn.close()
    connection = sql.connect('recipes.db')
    cur = connection.cursor()
    recipes = []
    for name in names:
        cur.execute("select recipe, ingredients, url FROM recipes where recipe = ?", name)
        recipes += cur.fetchall()
    connection.close()

    return render_template('favorites.html', recipes=recipes)

@app.route('/recipes')
def recipes():
    conn = sql.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT recipe, ingredients, url FROM recipes ")
    recipes = c.fetchall()
    conn.close()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes', methods=['POST'])
def add_to_favorites():
    try:
        recipe = request.form['recipe']
        
        conn = sql.connect('tb.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO favs(login_id, favorites) VALUES (?, ?)', (currUser, recipe))
        conn.commit()
        conn.close()

        conn = sql.connect('tb.db')
        c = conn.cursor()
        c.execute("SELECT favorites FROM favs where login_id = ?;", (currUser,))
        names = c.fetchall()
        conn.close()
        connection = sql.connect('recipes.db')
        cur = connection.cursor()
        recipes = []
        for name in names:
            cur.execute("select recipe, ingredients, url FROM recipes where recipe = ?", name)
            recipes += cur.fetchall()
        connection.close()

        return render_template('favorites.html', recipes=recipes)
    except:
        return render_template('login.html')


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
        error = {'firstname': 'First name is required.'}
    elif not lastname:
        error = {'lastname': 'Last name is required.'}
    elif not username:
        error = {'username': 'Username is required.'}
    elif not password:
        error = {'password': 'Password is required.'}
    elif check_username(username) == False:
        error = {'username': 'Username already exists.'}

    if error:
        return render_template('registration.html', error=error)

    enc_password = sha256_crypt.encrypt(password)
    
    # Insert the new user into the database
    with get_db() as con:
        cur = con.cursor()
        cur.execute("INSERT INTO logins (firstname, lastname, username, password) VALUES (?, ?, ?, ?)", (firstname, lastname, username, enc_password))
        con.commit()
    return render_template('index.html')

@app.route('/login_act', methods=['POST'])
def login_act():
    username = request.form['username']
    global currUser
    currUser = username
    password = request.form['password']
    error = None

    # Check if the provided username exists in the database
    with get_db() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM logins WHERE username=?", (username,))
        user = cur.fetchone()
        if user is None:
            # Username doesn't exist
            error = 'Incorrect username or password.'
        else:
            # Verify the user's password
            hashed_password = user[4] 
            if not sha256_crypt.verify(password, hashed_password):
                # Password doesn't match
                error = 'Incorrect username or password.'

    # If there was an error, show the login page again with an error message
    if error:
        return render_template('login.html', error=error)

    # Otherwise, the user is logged in, so redirect them to the index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5500)