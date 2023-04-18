import sqlite3


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


connection = sqlite3.connect('recipes.db')

cursor = connection.cursor()

cursor.execute('create table recipes (recipe varchar(100), ingredients varchar(10000), url varchar(200), cook_time varchar(30), date_published varchar(100), prep_time varchar(50), blurb varchar(240) );')



for recipe in recipes:
    try:
        str = ''
        str += 'insert into recipes values ("'
        str += recipe[0][6:min(len(recipe[0]), 100)]
        str += '","'
        str += recipe[1][13:min(len(recipe[1]), 10000)]
        str += '","'
        str += recipe[2][:min(len(recipe[2]), 200)]
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