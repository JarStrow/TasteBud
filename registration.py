from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
from passlib.hash import sha256_crypt
from flask import g
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import session

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'cs3203'

class User(UserMixin):
    pass

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    with get_db() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM logins WHERE id=?", (user_id,))
        user = cur.fetchone()
        if user is not None:
            user = User()
            user.id = user_id
        return user

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
@login_required
def favorites():
    username = session.get('username')
    conn = sql.connect('tb.db')
    c = conn.cursor()
    c.execute("SELECT favorites FROM favs where login_id = ?;", (username,))
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
@login_required
def add_to_favorites():
    try:
        recipe = request.form['recipe']
        username = session.get('username')
        
        conn = sql.connect('tb.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO favs(login_id, favorites) VALUES (?, ?)', (username, recipe))
        conn.commit()
        conn.close()

        conn = sql.connect('tb.db')
        c = conn.cursor()
        c.execute("SELECT favorites FROM favs where login_id = ?;", (username,))
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
@login_required
def settings():
    # Retrieve the logged-in user's username from the session
    username = session.get('username')

    # Fetch the user's information from the database using their username
    with get_db() as con:
        cur = con.cursor()
        cur.execute("SELECT firstname, lastname FROM logins WHERE username=?", (username,))
        user = cur.fetchone()

    # If the user is not found, redirect to the login page
    if user is None:
        return render_template("login.html")

    # Render the profile page with the user's information
    firstname = user[0]
    lastname = user[1]
    return render_template('settings.html', firstname=firstname, lastname=lastname)

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

from flask import session

@app.route('/login_act', methods=['POST'])
def login_act():
    username = request.form['username']
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
            else:
                # Log the user in
                user_obj = User()
                user_obj.id = user[0]
                login_user(user_obj)

                # Store the username in the session
                session['username'] = username

                return redirect(url_for('index'))
    
    # If there was an error, show the login page again with an error message
    if error:
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5500)