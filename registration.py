from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to your SQLite database
conn = sqlite3.connect('logins.db')
c = conn.cursor()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/index.html', methods=['POST'])
def register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    
    # Insert the form data into your database
    c.execute("INSERT INTO logins (firstname, lastname, username, password) VALUES (?, ?, ?, ?)", 
              (str(firstname), str(lastname), str(username), str(password)))
    conn.commit()
    
    # Close the cursor
    c.close()
    
    # Return the response
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)

# Close the database connection
conn.close()
