from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users\martin\PycharmProjects\Movie_Project/topmovies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'conejomalo'
KEY = 'fbb315277915128a7e9f0af1e7ac6fdf'
movies_title = []
dates = []
ides = []
img_url = []
description_url = []
Bootstrap(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    image_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.title


app.app_context().push()
db.create_all()


class MovieTitle(FlaskForm):
    title_movie = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


class MovieEdit(FlaskForm):
    rating = StringField('Rating')
    review = StringField('Review')
    submit = SubmitField('Add Movie')


@app.route('/', methods=["GET", "POST"])
def home():
    movies = Movies.query.order_by(Movies.rating).all()
    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i
    db.session.commit()
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    movie = MovieTitle()
    if movie.validate_on_submit():
        query = movie.title_movie.data
        API_URL = f"https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={query}"
        response = requests.get(API_URL)
        response_json = response.json()
        results = response_json['results']

        return render_template('select.html', movies=results)
    return render_template('add.html', movie=movie)


@app.route("/delete/<int:id>")
def delete(id):
    data = Movies.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


@app.route("/selectmovie")
def selectmovie():
    id_film = request.args.get("id")
    MOVIE_IMG = f'https://image.tmdb.org/t/p/w500'
    MOVIE_URL = f'https://api.themoviedb.org/3/movie/{id_film}?api_key={KEY}&language=en-US'
    response = requests.get(MOVIE_URL)
    selected_movie = response.json()
    new_film = Movies(
        title=selected_movie["title"],
        year=selected_movie["release_date"].split("-")[0],
        description=selected_movie["overview"],
        image_url=f"{MOVIE_IMG}{selected_movie['poster_path']}"
    )
    db.session.add(new_film)
    db.session.commit()
    return redirect(url_for("edit", id=new_film.id))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = MovieEdit()
    movie_id = request.args.get("id")
    new_movie = Movies.query.get(movie_id)
    if form.validate_on_submit():
        new_movie.rating = float(form.rating.data)
        new_movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", new_movie=new_movie, form=form)


if __name__ == '__main__':
    app.run(debug=True)
