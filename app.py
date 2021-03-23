from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import pymongo
from bson.binary import Binary
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_dropzone import Dropzone

# we can use ObjectId
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 2
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

dropzone = Dropzone(app)

cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('CLOUD_API_KEY'),
    api_secret=os.environ.get('CLOUD_API_SECRET')
)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'all_movies'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


def forms_validation():
    return ""


@app.route('/')
def show_landing_page():

    movieslist = []
    castname = ""
    directorname = ""

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:

        for movie in all_movies:

            name = movie['name'].lower()
            if result.lower() in name:
                movieslist.append(movie)
            for cast in movie['maincasts']:
                if (result.lower() in cast.lower()) and (result.lower()
                                                         not in name) and (cast.lower() not in directorname):
                    castname = cast.lower()
                    movieslist.append(movie)
            for director in movie['directors']:
                if (result.lower() in director.lower()) and (result.lower()
                                                             not in name) and (director.lower() not in castname):
                    directorname = director.lower()
                    movieslist.append(movie)

        print("/ route return 1")
        print(all_movies)

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=list(all_movies))

    else:
        print("/ route return 2")
        print(all_movies)

        return render_template('landingpage.template.html',
                               all_genre=list(all_genre),
                               all_movies=list(all_movies))


@ app.route('/', methods=['POST'])
def process_landing_page():

    name = request.form.get('name')
    genre = request.form.get('genre')
    imageurl = request.files['file']
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

    print("/ route return post")
    return redirect(url_for('show_landing_page'))


@ app.route('/<genre>/bygenre')
def show_movieinfolist_bygenre(genre):

    movieslist = []
    dbmovieslist = []

    castname = ""
    directorname = ""

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:

        for movie in all_movies:

            name = movie['name'].lower()
            if result.lower() in name:
                movieslist.append(movie)
            for cast in movie['maincasts']:
                if (result.lower() in cast.lower()) and (result.lower()
                                                         not in name) and (cast.lower() not in directorname):
                    castname = cast.lower()
                    movieslist.append(movie)
            for director in movie['directors']:
                if (result.lower() in director.lower()) and (result.lower()
                                                             not in name) and (director.lower() not in castname):
                    directorname = director.lower()
                    movieslist.append(movie)

            dbmovieslist.append(movie)

        print("/<genre>/bygenre route return 1")

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=dbmovieslist)
    else:

        for movie in all_movies:
            if movie['genre'] == genre:
                movieslist.append(movie)
            # need to append to a new list to retrieve the movie dict
            # else the all_movies will become undefined
            dbmovieslist.append(movie)

        print("/<genre>/bygenre route return 2")

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               movieslist=movieslist,
                               all_movies=dbmovieslist)


@ app.route('/<year>/byyear')
def show_movieinfolist_byyear(year):

    dbmovieslist = []
    movieslist = []

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')
    print(result)

    if result != None:

        for movie in all_movies:
            name = movie['name']
            if result in name:
                movieslist.append(movie)
            for cast in movie['maincasts']:
                if (result in cast) and (result not in name):
                    movieslist.append(movie)
            for director in movie['directors']:
                if result in director:
                    movieslist.append(movie)

            dbmovieslist.append(movie)

        print("/<year>/byyear route return 1")

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=dbmovieslist)

    else:

        for movie in all_movies:
            if movie['year'] == year:
                movieslist.append(movie)

            # need to append to a new list to retrieve the movie dict
            # else the all_movies will become undefined
            dbmovieslist.append(movie)

        print("/<year>/byyear route return 2")

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               movieslist=movieslist,
                               all_movies=dbmovieslist)


@app.route('/<movie_id>/movieinfo')
def show_movieinfo_page(movie_id):
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')
    print(result)

    if result != None:
        print("/<movie_id>/movieinfo route return 1")

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               all_movies=list(all_movies))
    else:
        movie = db.movies.find_one({
            '_id': ObjectId(movie_id)
        })
        print("/<movie_id>/movieinfo route return 2")

        return render_template('movieinfo.template.html',
                               all_genre=list(all_genre),
                               all_movies=list(all_movies),
                               movie=movie)


@app.route('/<movie_id>/movieinfo', methods=['POST'])
def process_delete_movieinfo(movie_id):
    movie = db.movies.find_one({
        '_id': ObjectId(movie_id)
    })

    name = movie['name']

    db.movies.remove({
        "_id": ObjectId(movie_id)
    })

    flash(name + " has been deleted!")

    print("/<movie_id>/movieinfo route return post")

    return redirect(url_for('show_landing_page'))


@app.route('/movieinfo/<movie_id>/update')
def show_update_movieinfo_page(movie_id):
    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    movie = db.movies.find_one({
        '_id': ObjectId(movie_id)
    })

    print("/<movie_id>/movieinfo/update route return")

    return render_template('movieinfo_update.template.html',
                           all_genre=list(all_genre),
                           all_movies=list(all_movies),
                           movie=movie)


@app.route('/movieinfo/<movie_id>/update', methods=['POST'])
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

    print("/<movie_id>/movieinfo/update route return post")
    return redirect(url_for('show_update_movieinfo_page', movie_id=movie_id))


if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),
    #         port=os.environ.get('PORT'), debug=True)
    app.run(host=os.environ.get('IP'),
            port=8080, debug=True)
