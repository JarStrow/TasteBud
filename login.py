import sqlite3

connection = sqlite3.connect('logins.db')

cursor = connection.cursor()

cursor.execute('select password from logins where username = "nathanstephani12";')

connection.commit()

print(cursor.fetchall())

connection.close()