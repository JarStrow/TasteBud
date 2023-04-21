
# Import from_db_cursor from prettytable library
from prettytable import from_db_cursor
# Import mysql connector
import sqlite3
# Import Error function from mysql.connector library
# Declare host, database, user, password attributes using a dictionary

# Check connectivity with the database
db = sqlite3.connect('recipes.db')


# Initiate cursor
cursor = db.cursor()
# Execute SQL query
cursor.execute("SELECT recipe, ingredients, url FROM recipes")
# Convert "gameRecords" table to a prettyTable
mytable = from_db_cursor(cursor)
# Generate the HTML code of the prettyTable using "get_html_string
htmlCode = mytable.get_html_string(attributes={"class":"table"}, format=True)
# Open prettyTable.html file
fo = open("recipes.html", "w")
# Write "htmlCode" to prettyTable.html
fo.write(htmlCode)
# Close prettyTable.html
fo.close()
