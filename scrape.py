import pymysql


def alphaNum(s):
    for l in s:
        if(l.isalpha() or l.isnumeric()):
            return True
    return False

def trim(s):
    new = ''
    for c in s:
        if(c != '"' and c != '}' and c != '{'):
            new += c
    return new

f = open('recipe.txt', 'r')
recipes = (f.read().strip()).split('}')

for i in range(len(recipes)):
    steps = recipes[i].split('", "')
    newsteps = []

    for step in steps:
        if(alphaNum(step)):
            step = step.replace("\\u2028", '')
            step = step.replace("\\n", " ")
            step = step.replace("\n", '')
            newsteps.append(trim(step))
    recipes[i] = newsteps


connection = pymysql.connect(host='localhost', user='nathan', password='password', database='TasteBud')

cursor = connection.cursor()

for i in range(1, 5):
    str = ''
    str += 'insert into recipes values ("'
    str += recipes[i][0]
    str += '","'
    str += recipes[i][1]
    str += '","'
    str += recipes[i][2]
    str += '","'
    str += recipes[i][3]
    str += '","'
    str += recipes[i][4]
    str += '","'
    str += recipes[i][5]
    str += '","'
    str += recipes[i][6]
    str += '","'
    str += recipes[i][7]
    str += '");'

    cursor.execute(str)

cursor.execute('select * from recipes')

results = cursor.fetchall()

for row in results:
    print(row)

connection.close()