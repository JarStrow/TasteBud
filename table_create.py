import sqlite3

# Open a connection to the database
conn = sqlite3.connect('recipes.db')
c = conn.cursor()

# Execute a SELECT query to retrieve the recipe data
c.execute('SELECT * FROM recipes')
recipes = c.fetchall()

# Generate an HTML table to display the recipe data
html = '<table>\n<tr>\n<th>Name</th>\n<th>Ingredients</th>\n<th>Instructions</th>\n</tr>\n'
for recipe in recipes:
    html += f'<tr>\n<td>{recipe[0]}</td>\n<td>{recipe[1]}</td>\n<td>{recipe[2]}</td>\n</tr>\n'
html += '</table>'

# Write the HTML code to a file
with open('recipes.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
    content="width=device-width, user-scalable=no, initial-scale=1.0, maximun-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>TasteBud</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />    
</head>
<body>
    <header>
        <div class="container">
            <nav class="nav">
                <ul class="nav nav-list-mobile">
                    <li class="nav-item">
                        <div class="mobile-menu">
                            <span class="line line-top"></span>
                            <span class="line line-bottom"></span>
                        </div>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link nav-link-logo"></a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link nav-link-profile"></a>
                    </li>
                </ul>
                <!-- ./nav-list nav-list-mobile -->
                <ul class="nav-list nav-list-larger">
                    <li class="nav-item nav-item-hidden">
                        <a href="/index.html" class="nav-link nav-link-logo"></a>
                    </li>
                    <li class="nav-item">
                        <a href="/recipes.html" class="nav-link">Recipes</a>
                    </li>
                    <li class="nav-item">
                        <a href="/ingredients.html" class="nav-link">Ingredients</a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link nav-link-search"></a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">Profile</a>
                        <ul class="nav-link-sub">
                            <li><a href="#">My Recipes</a></li>
                            <li><a href="#">Shopping List</a></li>
                            <li><a href="#">Edit Profile</a></li>
                            <li><a href="#">Settings</a></li>
                            <li><a href="#">Log In / Sign Up</a></li>
                        </ul>
                    </li>
                </ul>
                <!-- /.nav-list nav-list-larger -->
            </nav>
        </div>
    </header>
    <section class="recipes-page">
    <div class="container">
            <div class="title">
                <h2 class="title-heading">Recipes</h2>
            </div>
        </div>
    </section>
    <h1>Featured</h1>
    <p>This is a paragraph</p>
</body>
''')
    f.write(html)
    f.write('\n</body>\n</html>')
