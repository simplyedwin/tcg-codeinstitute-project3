from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import pymongo
from bson.binary import Binary

# we can use ObjectId
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'all_movies'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/movies')
def landing_page():
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()

    # files = os.listdir('./images')

    # for result in all_genre:
    #     print(result['genre'])
    return render_template('landingpage.template.html',
                           all_genre=all_genre,all_movies=all_movies)


@app.route('/movies/create')
def show_create_movie():
    # with open(path, 'rb') as f:
    #     contents = f.read()
    #     binary_file = Binary(contents)
    #     db.movie_thumbnails.insert_one({
    #         'name': 'RE',
    #         'file': binary_file
    #     })
    return render_template('create_movieinfo.template.html')


if __name__ == '__main__':
    print(os.listdir('./images'))
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'), debug=True)
