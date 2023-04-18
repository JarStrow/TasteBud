import sqlite3

connection = sqlite3.connect('logins.db')

cursor = connection.cursor()

def alphaNum(s):
    for l in s:
        if(l.isalpha() or l.isnumeric()):
            return True
    return False

def trim(s):
    new = ''
    for c in s:
        if(alphaNum(c)):
            new += c
    return new

def createuser():
    first = '"' + input("First Name (Maximum 20 characters):") + '"'
    last = '"' + input("Last Name (Maximum 20 characters):") + '"'
    username = '"' + input("Username (Maximum 50 characters):") + '"'
    if(len(username) > 52):
        print("Username must be 50 characters or less")
        createuser()
    password = input("Password (Maximum 20 characters, letters and numbers only):")
    check = input("Reenter password:")
    if(password != check or not(alphaNum(password)) or len(password) > 20):
        print("Passwords must match and contain only 20 letters/numbers")
        createuser()
    password = '"' + password + '"'

    log = 'insert into logins values (ff, ll, uu, pp);'
    log = log.replace('ff', first)
    log = log.replace('ll', last)
    log = log.replace('uu', username)
    log = log.replace('pp', password)
    
    cursor.execute(log)

    connection.commit()

def login():
    username = input('Enter Your Username\n')

    username = '"' + username + '"'

    print(username)
    password = input('Enter Your Password\n')

    log = 'select password from logins where username = uu ;'

    log = log.replace("uu", username)

    print(log)

    cursor.execute(log)

    correct = trim(str(cursor.fetchall()))

    if(password == correct):
        print('Success!')
    else:
        print('Error: Username or password incorrect')
        login()


createuser()
login()

connection.close()