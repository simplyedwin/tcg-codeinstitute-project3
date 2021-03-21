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

app.secret_key = os.environ.get('FLASK_SECRET_KEY')

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

    if request.args.get('result'):
        result = request.args.get('result')
        print(result)
        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               all_movies=list(all_movies))
    else:
        return render_template('landingpage.template.html',
                               all_genre=list(all_genre),
                               all_movies=list(all_movies))


@ app.route('/movies', methods=['POST'])
def process_landing_page():

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
        "youtubeurl": youtubeurl.replace('watch?v=', 'embed/')
    })

    flash(name + " has been added!")
    return redirect(url_for('show_landing_page'))


@ app.route('/movies/<genre>/bygenre')
def show_movieinfolist_bygenre(genre):
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    return render_template('movieinfolist.template.html',
                           all_genre=list(all_genre),
                           genre=genre,
                           all_movies=list(all_movies))


@ app.route('/movies/<year>/byyear')
def show_movieinfolist_byyear(year):
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    return render_template('movieinfolist.template.html',
                           all_genre=list(all_genre),
                           year=year,
                           all_movies=list(all_movies))


# @ app.route('/movies')
# def show_movieinfolist_byresult():

#     print("Hello")
#     result = request.args.get('result')
#     print(type(result))
#     all_genre = db.movie_genres.find()
#     all_movies = db.movies.find()
#     return render_template('movieinfolist.template.html',
#                            all_genre=list(all_genre),
#                            result=result,
#                            all_movies=list(all_movies))


@app.route('/movies/<movie_id>/movieinfo')
def show_movieinfo_page(movie_id):
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    movie = db.movies.find_one({
        '_id': ObjectId(movie_id)
    })

    return render_template('movieinfo.template.html',
                           all_genre=list(all_genre),
                           all_movies=list(all_movies),
                           movie=movie)


@app.route('/movies/<movie_id>/movieinfo', methods=['POST'])
def process_delete_movieinfo(movie_id):
    movie = db.movies.find_one({
        '_id': ObjectId(movie_id)
    })

    name = movie['name']

    db.movies.remove({
        "_id": ObjectId(movie_id)
    })

    flash(name + " has been deleted!")
    return redirect(url_for('show_landing_page'))


@app.route('/movies/movieinfo/<movie_id>/update')
def show_update_movieinfo_page(movie_id):
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    movie = db.movies.find_one({
        '_id': ObjectId(movie_id)
    })

    return render_template('movieinfo_update.template.html',
                           all_genre=list(all_genre),
                           all_movies=list(all_movies),
                           movie=movie)


@app.route('/movies/movieinfo/<movie_id>/update', methods=['POST'])
def process_update_movieinfo_page(movie_id):

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

    db.movies.update_one({
        "_id": ObjectId(movie_id)
    }, {
        '$set': {
            "name": name,
            "genre": genre.lower(),
            "imageurl": result['url'],
            "year": year,
            "maincasts": maincasts.split(","),
            "synopsis": synopsis,
            "directors": directors.split(","),
            "youtubeurl": youtubeurl.replace('watch?v=', 'embed/')
        }
    })

    flash(name + " has been updated!")
    return redirect(url_for('show_update_movieinfo_page', movie_id=movie_id))


if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),
    #         port=os.environ.get('PORT'), debug=True)
    app.run(host=os.environ.get('IP'),
            port=8080, debug=True)
