import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('recipes.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the recipe table if it doesn't already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS recipes
                  (name TEXT, ingredients TEXT, instructions TEXT)''')

# Add some sample data to the table
cursor.execute("INSERT INTO recipes VALUES ('Pizza', 'Pepperoni, Cheese, Sauce', 'Bake in oven')")
cursor.execute("INSERT INTO recipes VALUES ('Chicken Parmesan', 'Chicken, Parmesan', 'Mix and fry')")
cursor.execute("INSERT INTO recipes VALUES ('Banana Pudding', 'Bananas, Pudding Mix', 'Mix and chill')")

# Commit the changes to the database and close the connection
conn.commit()
conn.close()
