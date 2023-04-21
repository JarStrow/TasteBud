from flask import Flask, request, render_template
import sqlite3 as sql
app = Flask(__name__, static_url_path='/static')

conn = sql.connect('logins.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS logins (firstname TEXT NOT NULL, lastname TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)')
print("Table created successfully")
conn.close()

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

@app.route('/addrec',methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            password  = request.form['password']
        
            with sql.connect('logins.db') as con:
                cur = con.cursor()

                cur.execute("INSERT INTO logins (firstname, lastname, username, password) VALUES (?,?,?,?)", (firstname, lastname, username, password))
                print("Added to table successfully")

                con.commit()
                msg = "Record added"
        except:
            con.rollback()
            msg = "error in insert operation"
        
        finally:
            con.close()
            return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=5500)