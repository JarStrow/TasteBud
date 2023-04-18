from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Connect to your SQLite database
conn = sqlite3.connect('logins.db')
c = conn.cursor()

@app.route('/registration', methods=['POST'])
def register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    
    # Insert the form data into your database
    c.execute("INSERT INTO users (firstname, lastname, username, password) VALUES (?, ?, ?, ?)", 
              (firstname, lastname, username, password))
    conn.commit()
    
    # Close the database connection
    c.close()
    conn.close()
    
    # Redirect to success page or login page
    return 'Registration successful!'

if __name__ == '__main__':
    app.run(debug=True)
