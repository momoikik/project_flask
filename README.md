![Image](https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg)

# S-IMDB

Simple Internet Movies DataBase

# Description
a database site for movies. 
Similar to the popular site of IMDB, 
but a little bit simpler.
---
## Client
* HTML 
1) index.html - the home web page which contain the main movies page, including movie pictures
2) movie_info.html - a web page containing the movie information
3) add_profile.html - a web page for adding new movie
4) alter_movie.html - a web page for editing an existing movie
* CSS
1) style.css - a cascade style sheet coneected with index.html, and movie_info.html
## Server
* Flask
## Database
* SQLite
---
# Installation
Run the following in pyCharm Terminal:
```bash
pip install flask
pip install flask-sqlalchemy
pip install Flask-Migrate
```
# Usage
* Open the S-IMDB site: http://127.0.0.1:5000
* Click on the correspponding movie picture to open the movie info web page
* In the movie info web page
1) you can "delete" current movie
2) "alter" it by clicking on the corresponding link
3) Add Comments in the "Name" + "Review" sections and clicking "ADD" button
* To add a new movie
1) click on this URL:http://127.0.0.1:5000/add_data
2) Fill in the movie info
3) Click on the "ADD" button

# Application Development
app.py
1) Created a new SQLite DB 'movies.db'
2) Created a new class: Movies to be used for representing Movies table in DB
3) Created a new class: Reviews to be used for representing Reviews table in DB
4) Routed all relevant URLs to the relevant code:
* /
* /add_data
* /add
* /delete
* /display/<filename>
* movie_info/<movie_id>
* /add_review
* /delete/<int:id>
* /alter_movie/<int:id>", methods=["POST", "GET"]

# Authors and acknowledgment
Marjan Ikteelat

# License
the software is free under GPL(General Public License)#   p r o j e c t _ f l a s k  
 