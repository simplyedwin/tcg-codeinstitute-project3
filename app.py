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


def validate_form(form):

    print("Validation in progress...")

    errors = {}

    name = request.form.get('name')
    genre = request.form.get('genre')
    imageurl = request.files['file']
    year_string = request.form.get('year')
    maincasts = request.form.get('maincasts')
    synopsis = request.form.get('synopsis')
    directors = request.form.get('directors')
    youtubeurl = request.form.get('youtubeurl')
    backdrop = request.files['backdrop']
    thumbnails = request.files['thumbnails']

    if len(name) == 0:
        errors['title_is_blank'] = "Movie title field cannot be blank"

    if len(genre) == 0:
        errors['genre_is_blank'] = "Genre field cannot be blank"

    if len(year_string) == 0:
        errors['year_is_blank'] = "Year field cannot be blank"

    try:
        print("year is not string")
        year = int(year_string)

        if year <= 0:
            errors['year_is_less_than_0'] = "Year field cannot be less than or equal to zero"

    except:
        print("year is string")
        errors['year_is_string'] = "Year field cannot be words or characters"

    if len(synopsis) == 0:
        errors['synopsis_is_blank'] = "Synopsis field cannot be blank"

    if len(maincasts) == 0:
        errors['maincasts_is_blank'] = "Maincasts field cannot be blank"

    if len(directors) == 0:
        errors['directors_is_blank'] = "Directors field cannot be blank"

    if len(youtubeurl) == 0:
        errors['youtubeurl_is_blank'] = "Youtubeurl field cannot be blank"

    if len(imageurl.filename) == 0:
        errors['file_is_blank'] = "Poster field cannot be blank"

    if len(backdrop.filename) == 0:
        errors['backdrop_is_blank'] = "Backdrop field cannot be blank"

    if len(thumbnails.filename) == 0:
        errors['thumbnails_is_blank'] = "Thumbnails field cannot be blank"

    return errors


def search_result(result, all_movies, castname, directorname, movieslist, dbmovieslist):

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

    return movieslist, dbmovieslist


@app.route('/')
def show_landing_page():

    dbmovieslist = []
    movieslist = []
    castname = ""
    directorname = ""

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:

        movieslist, dbmovieslist = search_result(
            result, all_movies, castname, directorname, movieslist, dbmovieslist)

        print("/ route return 1")
        print(all_movies)

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=dbmovieslist, old_values={}, errors={})

    else:
        print("/ route return 2")
        return render_template('landingpage.template.html',
                               all_genre=list(all_genre),
                               all_movies=list(all_movies), old_values={}, errors={})


@ app.route('/', methods=['POST'])
def process_landing_page():

    result_thumbnails = []
    errors = validate_form(request.form)

    if len(errors) == 0:

        name = request.form.get('name')
        genre = request.form.get('genre')
        imageurl = request.files['file']
        year = request.form.get('year')
        maincasts = request.form.get('maincasts')
        synopsis = request.form.get('synopsis')
        directors = request.form.get('directors')
        youtubeurl = request.form.get('youtubeurl')
        backdrop = request.files['backdrop']
        thumbnails = request.files.getlist("thumbnails")

        result_poster = cloudinary.uploader.upload(imageurl.stream,
                                                   public_id=name,
                                                   folder="tcgproj3/"+genre+"/"+name,
                                                   resource_type="image"
                                                   )

        result_backdrop = cloudinary.uploader.upload(backdrop.stream,
                                                     public_id=name,
                                                     folder="tcgproj3/"+genre+"/"+name,
                                                     resource_type="image"
                                                     )
        for i in range(len(thumbnails)):

            result_thumbnail = cloudinary.uploader.upload(thumbnails[i].stream,
                                                          public_id=name +
                                                          "tn"+str(i+1),
                                                          folder="tcgproj3/"+genre+"/"+name,
                                                          resource_type="image"
                                                          )
            result_thumbnails.append(result_thumbnail['url'])

        db.movies.insert_one({
            "name": name,
            "genre": genre.lower(),
            "imageurl": result_poster['url'],
            "year": year,
            "maincasts": maincasts.split(","),
            "synopsis": synopsis,
            "directors": directors.split(","),
            "youtubeurl": youtubeurl.replace('watch?v=', 'embed/'),
            'backdrop': result_backdrop['url'],
            'thumbnails': result_thumbnails
        })

        flash(name + " has been added!")

        print("/ route return post")
        return redirect(url_for('show_landing_page'))

    else:
        for k, v in errors.items():
            flash(v)
        all_genre = db.movie_genres.find()
        all_movies = db.movies.find()

        print("/create route errors")
        return render_template('landingpage.template.html',
                               all_movies=list(all_movies),
                               all_genre=list(all_genre),
                               errors=errors,
                               old_values=request.form)


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

        movieslist, dbmovieslist = search_result(
            result, all_movies, castname, directorname, movieslist, dbmovieslist)

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=dbmovieslist, old_values={}, errors={})

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
                               all_movies=dbmovieslist, old_values={}, errors={})


@ app.route('/<year>/byyear')
def show_movieinfolist_byyear(year):

    dbmovieslist = []
    movieslist = []

    castname = ""
    directorname = ""

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')
    print(result)

    if result != None:

        movieslist, dbmovieslist = search_result(
            result, all_movies, castname, directorname, movieslist, dbmovieslist)

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=dbmovieslist, old_values={}, errors={})

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
                               all_movies=dbmovieslist, old_values={}, errors={})


@app.route('/<movie_id>/movieinfo')
def show_movieinfo_page(movie_id):

    dbmovieslist = []
    movieslist = []

    castname = ""
    directorname = ""

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:
        # print("/<movie_id>/movieinfo route return 1")
        movieslist, dbmovieslist = search_result(
            result, all_movies, castname, directorname, movieslist, dbmovieslist)

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=dbmovieslist, old_values={}, errors={})
    else:
        movie = db.movies.find_one({
            '_id': ObjectId(movie_id)
        })
        print("/<movie_id>/movieinfo route return 2")

        return render_template('movieinfo.template.html',
                               all_genre=list(all_genre),
                               all_movies=list(all_movies),
                               old_values=movie, errors={})


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

    dbmovieslist = []
    movieslist = []

    castname = ""
    directorname = ""

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:
        # print("/<movie_id>/movieinfo route return 1")
        movieslist, dbmovieslist = search_result(
            result, all_movies, castname, directorname, movieslist, dbmovieslist)

        return render_template('movieinfolist.template.html',
                               all_genre=list(all_genre),
                               result=result,
                               movieslist=movieslist,
                               all_movies=dbmovieslist, old_values={}, errors={})
    else:
        movie = db.movies.find_one({
            '_id': ObjectId(movie_id)
        })

        print("/<movie_id>/movieinfo/update route return")

        return render_template('movieinfo.template.html',
                               all_genre=list(all_genre),
                               all_movies=list(all_movies),
                               old_values=movie, errors={})


@app.route('/movieinfo/<movie_id>/update', methods=['POST'])
def process_update_movieinfo_page(movie_id):

    result_thumbnails = []
    errors = validate_form(request.form)

    print("Error length: {}".format(len(errors)))

    if len(errors) == 0:

        name = request.form.get('name')
        genre = request.form.get('genre')
        imageurl = request.files['file']
        year = request.form.get('year')
        maincasts = request.form.get('maincasts')
        synopsis = request.form.get('synopsis')
        directors = request.form.get('directors')
        youtubeurl = request.form.get('youtubeurl')
        backdrop = request.files['backdrop']
        thumbnails = request.files.getlist("thumbnails")

        result_poster = cloudinary.uploader.upload(imageurl.stream,
                                                   public_id=name,
                                                   folder="tcgproj3/"+genre+"/"+name,
                                                   resource_type="image"
                                                   )

        result_backdrop = cloudinary.uploader.upload(backdrop.stream,
                                                     public_id=name,
                                                     folder="tcgproj3/"+genre+"/"+name,
                                                     resource_type="image"
                                                     )
        for i in range(len(thumbnails)):

            result_thumbnail = cloudinary.uploader.upload(thumbnails[i].stream,
                                                          public_id=name +
                                                          "tn"+str(i+1),
                                                          folder="tcgproj3/"+genre+"/"+name,
                                                          resource_type="image"
                                                          )
            result_thumbnails.append(result_thumbnail['url'])

        db.movies.update_one({
            "_id": ObjectId(movie_id)
        }, {
            '$set': {
                "name": name,
                "genre": genre.lower(),
                "imageurl": result_poster['url'],
                "year": year,
                "maincasts": maincasts.split(","),
                "synopsis": synopsis,
                "directors": directors.split(","),
                "youtubeurl": youtubeurl.replace('watch?v=', 'embed/'),
                'backdrop': result_backdrop['url'],
                'thumbnails': result_thumbnails
            }
        })

        flash(name + " has been updated!")

        print("/<movie_id>/movieinfo/update route return post")
        return redirect(url_for('show_update_movieinfo_page', movie_id=movie_id))

    else:

        for k, v in errors.items():
            flash(v)

        movie = db.movies.find_one({
            '_id': ObjectId(movie_id)
        })

        all_genre = db.movie_genres.find()
        all_movies = db.movies.find()
        old_values = {**movie, **request.form}

        print("/create route errors")
        return render_template('movieinfo.template.html',
                               all_movies=list(all_movies),
                               all_genre=list(all_genre),
                               errors=errors,
                               old_values=old_values)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('custom404.template.html')


if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),
    #         port=os.environ.get('PORT'), debug=True)
    app.run(host=os.environ.get('IP'),
            port=8080, debug=True)
