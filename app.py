from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import pymongo
from bson.binary import Binary
import cloudinary
import cloudinary.uploader
import cloudinary.api

# we can use ObjectId
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('CLOUD_API_KEY'),
    api_secret=os.environ.get('CLOUD_API_SECRET')
)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'all_movies'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/movies')
def show_landing_page():
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    return render_template('landingpage.template.html',
                           all_genre=list(all_genre),
                           all_movies=list(all_movies))


@app.route('/movies', methods=['POST'])
def process_landing_page():

    visible = True

    name = request.form.get('name')
    genre = request.form.get('genre')
    imageurl = request.files['imageurl']
    year = request.form.get('year')
    maincasts = request.form.get('maincasts')
    synopsis = request.form.get('synopsis')
    directors = request.form.get('directors')
    youtubeurl = request.form.get('youtubeurl')

    result = cloudinary.uploader.upload(imageurl.stream,
                                        public_id=name,
                                        folder="tcgproj3/"+genre+"/"+name,
                                        resource_type="image"
                                        )

    db.movies.insert_one({
        "name": name,
        "genre": genre.lower(),
        "imageurl": result['url'],
        "year": year,
        "maincasts": maincasts.split(","),
        "synopsis": synopsis,
        "directors": directors.split(","),
        "youtubeurl": youtubeurl
    })

    return render_template('landingpage.template.html')


@app.route('/movies/<genre>/bygenre')
def show_movieinfolist_bygenre(genre):

    all_movies = db.movies.find()
    return render_template('movieinfolist.template.html',
                           genre=genre,
                           all_movies=list(all_movies))


@app.route('/movies/<movie_id>/movieinfo')
def show_movieinfo_page(movie_id):
    movie = db.movies.find_one({
        '_id': ObjectId(movie_id)
    })

    return render_template('movieinfo.template.html',
                           movie=movie)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'), debug=True)
