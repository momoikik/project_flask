from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import random,string
def randomword(length):
    letters=string.ascii_letters
    return ''.join(random.choice(letters)for i in range(length))
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = ['png', 'jpeg', 'jpg', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db = SQLAlchemy(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False)
    director = db.Column(db.String(20), unique=False, nullable=False)
    release_year = db.Column(db.Integer, unique=False, nullable=False)
    filename = db.Column(db.String(100), unique=False, nullable=True)
    actors = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return f"Title: {self.movie_title}, Director: {self.director}"


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    review_text = db.Column(db.String, unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return f"Name: {self.name}, Content: {self.review_text}"


migrate = Migrate(app, db)


@app.route("/")
def home():
    movies_data = Movies.query.all()
    return render_template("index.html", movies_data=movies_data)


@app.route("/add_data")
def add_data():
    return render_template("add_profile.html")


@app.route("/add", methods=["POST", "GET"])
def movie_management():
    if request.method == "POST":
        movie_title = request.form.get("movie_title")
        description = request.form.get("description")
        director = request.form.get("director")
        release_year = request.form.get("release_year")
        actors = request.form.get("actors")
        file = request.files.get("filename")
        randomstring=randomword(10)
        if allowed_file(file.filename):
            file_split= file.filename.split(".")
            file_name = f"{file_split[0]}_{randomstring}.{file_split[1]}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
        file_name = f"{file_split[0]}_{randomstring}.{file_split[1]}"
        movie_row = Movies(movie_title=movie_title, description=description, director=director,
                           release_year=release_year, filename=file_name, actors=actors)
        db.session.add(movie_row)
        db.session.commit()
        return redirect("/")


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename))


@app.route('/movie_info/<movie_id>')
def movie_info(movie_id):
    movie_specific = Movies.query.get(movie_id)
    reviews_specific = Reviews.query.filter(Reviews.movie_id == movie_id)
    return render_template("movie_info.html", movie_specific=movie_specific, reviews_specific=reviews_specific)


@app.route("/add_review", methods=["POST"])
def review_management():
    if request.method == "POST":
        name = request.form.get("name")
        review_text = request.form.get("review_text")
        rating = request.form.get("rating")
        movie_id = request.form.get("movie_id")

        review_row = Reviews(name=name, review_text=review_text,rating =rating, movie_id=movie_id)
        db.session.add(review_row)
        db.session.commit()
        return redirect("/movie_info/" + movie_id)


@app.route("/delete/<int:id>")
def erase(id):
    data = Movies.query.get(id)
    filename = data.filename
    os.remove(f"{app.config['UPLOAD_FOLDER']}/{filename}")
    db.session.delete(data)
    reviews_specific = Reviews.query.filter(Reviews.movie_id == id)
    for review in reviews_specific:
        db.session.delete(review)
    db.session.commit()
    return redirect("/")


@app.route("/alter_movie/<int:id>", methods=["POST", "GET"])
def alter_movie(id):
    if request.method == "POST":
        data = Movies.query.get(id)
        movie_title = request.form.get("movie_title")
        description = request.form.get("description")
        director = request.form.get("director")
        release_year = request.form.get("release_year")
        actors = request.form.get("actors")
        file = request.files.get("filename")
        if allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        file_name = file.filename
        if request.form.get("movie_title"):
            data.movie_title = movie_title
        if request.form.get("description"):
            data.description = description
        if request.form.get("director"):
            data.director = director
        if request.form.get("release_year"):
            data.release_year = release_year
        if request.form.get("actors"):
            data.actors = actors
        if request.files.get("filename"):
            data.filename = file_name

        db.session.commit()
        return redirect(url_for('movie_info', movie_id=id))
    else:
        return render_template("alter_movie.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        movies_data = Movies.query.filter(Movies.movie_title.like(search)).all()

        return render_template('index.html', movies_data=movies_data, pageTitle='Movies', legend="Search Results")
    else:
        return redirect("/")
if __name__ == "__main__":
    app.run()
