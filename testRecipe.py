import sqlite3
import html

# connect to the database
conn = sqlite3.connect('recipes.db')

# get a cursor object
cursor = conn.cursor()

# execute a SELECT statement on the table
cursor.execute("SELECT recipe, ingredients FROM recipes")

# create an empty list to hold the rows of data
rows = []

# iterate over the rows returned by the SELECT statement
for row in cursor.fetchall():
    # add each row to the list as a tuple of values
    rows.append((row[0], row[1]))

# create an HTML table to display the data
table_html = '<table>\n'
for row in rows:
    table_html += '<tr>\n'
    for col in row:
        table_html += f'<td>{html.escape(str(col))}</td>\n'
    table_html += '</tr>\n'
table_html += '</table>'

# print the HTML table
print(table_html)

# close the database connection
conn.close()
