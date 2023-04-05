
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

print(len(recipes))
print(recipes[0])