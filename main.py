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
KEY = 'fbb315277915128a7e9f0af1e7ac6fdf'
movies_title = []
dates = []
ides = []
Bootstrap(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    image_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.title


app.app_context().push()
#db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    movies = Movies.query.all()
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        movies_title.clear()
        dates.clear()
        ides.clear()
        title = request.form['title']
        year = request.form['year']
        description = request.form['description']
        rating = request.form['rating']
        ranking = request.form['ranking']
        review = request.form['review']
        image_url = request.form['image_url']
        query = title
        API_URL = f"https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={query}"
        response = requests.get(API_URL)
        response_json = response.json()
        results = response_json['results']
        final = len(results)
        for i in range(0, final):
            new_results = results[i]['original_title']
            new_dates = results[i]['release_date']
            new_ids = results[i]['id']
            movies_title.append(new_results)
            dates.append(new_dates)
            ides.append(new_ids)
        print(movies_title)
        print(dates)
        print(ides)
        return render_template('select.html', movies=movies_title, dates=dates, final=final, ides=ides, results=results)

    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        movie_id = request.form["id"]
        movie_update = Movies.query.get(movie_id)
        movie_update.rating = request.form["rating"]
        movie_update.review = request.form["review"]
        db.session.commit()
        return redirect('/')
    movie_id = request.args.get('id')
    movie_selected = Movies.query.get(movie_id)
    return render_template("edit.html", data=movie_selected)


@app.route("/delete/<int:id>")
def delete(id):
    data = Movies.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


@app.route("/", methods=["GET", "POST"])
def select():
    return render_template("select.html")


if __name__ == '__main__':
    app.run(debug=True)
