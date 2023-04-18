import sqlite3

connection = sqlite3.connect('recipes.db')

cursor = connection.cursor()

cursor.execute("select recipe from recipes where ingredients like '% chicken %'")

results = cursor.fetchall()

for line in results:
    print(line)

connection.close()