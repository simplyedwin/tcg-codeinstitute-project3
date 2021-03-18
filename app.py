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
  cloud_name = os.environ.get('CLOUD_NAME'), 
  api_key = os.environ.get('CLOUD_API_KEY'), 
  api_secret = os.environ.get('CLOUD_API_SECRET') 
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

    name = request.form.get('name')
    genre = request.form.get('genre')
    imageurl = request.form.get('imageurl')
    year = request.form.get('year')
    maincasts = request.form.get('maincasts')
    synopsis = request.form.get('synopsis')
    directors = request.form.get('directors')
    youtubeurl = request.form.get('youtubeurl')

    return redirect(url_for('show_landing_page'))


@app.route('/movies/bygenre')
def show_create_movie():
    return render_template('create_movieinfo.template.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'), debug=True)
