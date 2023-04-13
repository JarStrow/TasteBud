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

for recipe in recipes:
    try:
        str = ''
        str += 'insert into recipes values ("'
        str += recipe[0][:min(len(recipe[0]), 100)]
        str += '","'
        str += recipe[1][:min(len(recipe[1]), 10000)]
        str += '","'
        str += recipe[2][:min(len(recipe[2]), 200)]
        str += '","'
        str += recipe[3][:min(len(recipe[3]), 200)]
        str += '","'
        str += recipe[4][:min(len(recipe[4]), 30)]
        str += '","'
        str += recipe[5][:min(len(recipe[5]), 100)]
        str += '","'
        str += recipe[6][:min(len(recipe[6]), 50)]
        str += '","'
        str += recipe[7][:min(len(recipe[7]), 240)]
        str += '");'
    except:
        continue

    cursor.execute(str)

connection.commit()

cursor.execute('select * from recipes')

results = cursor.fetchall()

for row in results:
    print(row)

connection.close()