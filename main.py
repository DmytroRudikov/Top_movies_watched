import sqlalchemy.orm.query
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

MOVIE_DB_KEY = os.getenv("MOVIE_DB_KEY")
movies_online_dtb = "https://api.themoviedb.org/3"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class EditForm(FlaskForm):
    new_rating_field = StringField(label="Your Rating Out of 10 e.g. 7.5")
    new_review_field = StringField(label="Your Review")
    submit = SubmitField(label="Done")


class AddNewFilmForm(FlaskForm):
    movie_name = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, unique=True, nullable=False)


db.create_all()


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating.desc()).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    movie_id = request.args.get("movie_id")
    to_edit = Movie.query.get(movie_id)
    if form.validate_on_submit():
        to_edit.rating = form.new_rating_field.data
        to_edit.review = form.new_review_field.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=to_edit)


@app.route("/delete")
def delete():
    movie_id = request.args.get("movie_id")
    to_delete = Movie.query.get(movie_id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddNewFilmForm()
    if form.validate_on_submit():
        parameters = {
            "api_key": MOVIE_DB_KEY,
            "query": form.movie_name.data,
        }
        suggested_films = requests.get(f"{movies_online_dtb}/search/movie", params=parameters).json()["results"]
        return render_template("select.html", movies=suggested_films)
    return render_template("add.html", form=form)


@app.route("/select")
def select():
    selected_movie = request.args.get("selected_movie")
    parameters = {
        "api_key": MOVIE_DB_KEY,
    }
    selected_movie_data = requests.get(f"{movies_online_dtb}/movie/{selected_movie}", params=parameters).json()
    movie_title = selected_movie_data["title"]
    movie_poster = f"https://www.themoviedb.org/t/p/original{selected_movie_data['poster_path']}"
    release_year = selected_movie_data["release_date"].split("-")[0]
    description = selected_movie_data["overview"]
    movie_to_add = Movie(title=movie_title, year=release_year, description=description, img_url=movie_poster)
    db.session.add(movie_to_add)
    db.session.commit()
    return redirect(url_for("edit", movie_id=movie_to_add.id))


if __name__ == '__main__':
    app.run(debug=True)
