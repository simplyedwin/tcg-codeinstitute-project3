from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
import os
from dotenv import load_dotenv
import pymongo
from bson.binary import Binary
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_dropzone import Dropzone
import requests
from werkzeug.wrappers import BaseResponse as Response

# we can use ObjectId
from bson.objectid import ObjectId

load_dotenv()

IP = os.environ.get('IP')
PORT = os.environ.get('PORT')

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

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
    thumbnails = request.files.getlist("thumbnails")

    thumbnails_size = 0
    poster_size = len(imageurl.read())
    backdrop_size = len(backdrop.read())
    for tn in thumbnails:
        thumbnails_size = thumbnails_size + len(tn.read())
    print(imageurl)
    print("Poster size is {} ".format(poster_size))
    print(backdrop)
    print("Backdrop size is {} ".format((backdrop_size)))
    print(thumbnails)
    print("Thumbnails size is {}".format(thumbnails_size))

    if len(name) == 0 or name.isspace():
        errors['title_is_blank'] = "Movie title field cannot be blank"

    if len(genre) == 0 or genre.isspace():
        errors['genre_is_blank'] = "Genre field cannot be blank"

    if len(year_string) == 0 or year_string.isspace():
        errors['year_is_blank'] = "Year field cannot be blank"

    try:
        print("year is not string")
        year = int(year_string)

        if year <= 0:
            errors['year_is_less_than_0'] = "Year field cannot be less than or equal to zero"

    except:
        print("year is string")
        errors['year_is_string'] = "Year field cannot be words or characters"

    if len(synopsis) == 0 or synopsis.isspace():
        errors['synopsis_is_blank'] = "Synopsis field cannot be blank"

    if len(maincasts) == 0 or maincasts.isspace():
        errors['maincasts_is_blank'] = "Maincasts field cannot be blank"

    if len(directors) == 0 or directors.isspace():
        errors['directors_is_blank'] = "Directors field cannot be blank"

    if len(youtubeurl) == 0 or youtubeurl.isspace():
        errors['youtubeurl_is_blank'] = "Trailer (Youtube url) field cannot be blank"
    else:
        if ('watch?v=' in youtubeurl) or ('embed/' in youtubeurl):
            pass
        else:
            errors['youtubeurl_format_wrong'] = "Trailer (Youtube url) format is incorrect"

    if len(imageurl.filename) == 0:
        errors['file_is_blank'] = "Poster field cannot be blank"
    elif '.' in imageurl.filename:
        file_ext = os.path.splitext(imageurl.filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            errors['poster_ext_is_wrong'] = "Poster file ext is invalid"
    elif poster_size > 1024 * 1024:
        errors['poster_size_above_limit'] = "Poster file size cannot be  more than 1MB"

    if len(backdrop.filename) == 0:
        errors['backdrop_is_blank'] = "Backdrop field cannot be blank"
    elif '.' in backdrop.filename:
        file_ext = os.path.splitext(backdrop.filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            errors['bkdrp_ext_is_wrong'] = "Backdrop file ext is invalid"
    elif backdrop_size > 1024 * 1024:
        errors['backdrop_size_above_limit'] = "Backdrop file size cannot be more than 1MB"

    if len(thumbnails) == 0:
        errors['thumbnails_is_blank'] = "Thumbnails field cannot be blank"
    elif thumbnails_size > 1024 * 1024 * 2:
        errors['thumbnails_size_above_limit'] = "Thumbnails files size cannot be more than 2MB"
    else:
        for tn in thumbnails:
            if '.' in tn.filename:
                file_ext = os.path.splitext(backdrop.filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    errors['thn_ext_is_wrong'] = "Thumbnail files ext are invalid"

    return errors


def search_result(result, all_movies, movieslist, dbmovieslist):

    for movie in all_movies:

        name = movie['name'].lower()
        maincasts = movie['maincasts']
        directors = movie['directors']

        if result.lower() in name:
            movieslist.append(movie)

        for cast in maincasts:
            if (result.lower() in cast.lower()) and (result.lower() not in name):
                movieslist.append(movie)

        for director in directors:
            if (result.lower() in director.lower()) and (result.lower() not in name):
                movieslist.append(movie)

        dbmovieslist.append(movie)

    movieslist = list({v['_id']: v for v in movieslist}.values())

    return movieslist, dbmovieslist


@ app.route('/')
def show_landing_page():

    dbmovieslist = []
    movieslist = []

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:

        movieslist, dbmovieslist = search_result(
            result, all_movies, movieslist, dbmovieslist)

        if not movieslist:
            flash("Sorry we found no result for {}".format(result))

            return redirect(url_for('show_landing_page'))

        else:

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

    url = request.url
    response = requests.get(url)
    status_code = int(response.status_code)

    movie_title = request.form.get('name')
    movie_genre = request.form.get('genre')
    movie_imageurl = request.files['file']
    movie_year = request.form.get('year')
    movie_maincasts = request.form.get('maincasts')
    movie_synopsis = request.form.get('synopsis')
    movie_directors = request.form.get('directors')
    movie_youtubeurl = request.form.get('youtubeurl')
    movie_backdrop = request.files['backdrop']
    movie_thumbnails = request.files.getlist("thumbnails")

    errors = validate_form(request.form)

    result_thumbnails = []

    uploaded__movie_youtubeurl = ""

    if len(errors) == 0 and status_code == 200:

        movie_title = request.form.get('name')
        movie_genre = request.form.get('genre')
        movie_imageurl = request.files['file']
        movie_year = request.form.get('year')
        movie_maincasts = request.form.get('maincasts')
        movie_synopsis = request.form.get('synopsis')
        movie_directors = request.form.get('directors')
        movie_youtubeurl = request.form.get('youtubeurl')
        movie_backdrop = request.files['backdrop']
        movie_thumbnails = request.files.getlist("thumbnails")

        movie_imageurl.seek(0)
        movie_backdrop.seek(0)

        # poster_size = len(movie_imageurl.read())

        # print("line 223 {} is of size {}".format(
        #     movie_imageurl.filename, poster_size))

        result_poster = cloudinary.uploader.upload(movie_imageurl.stream,
                                                   public_id=movie_title+"_poster",
                                                   folder="tcgproj3/"+movie_genre+"/"+movie_title,
                                                   resource_type="image"
                                                   )

        result_backdrop = cloudinary.uploader.upload(movie_backdrop.stream,
                                                     public_id=movie_title+"_backdrop",
                                                     folder="tcgproj3/"+movie_genre+"/"+movie_title,
                                                     resource_type="image"
                                                     )
        for i in range(len(movie_thumbnails)):

            movie_thumbnails[i].seek(0)

            result_thumbnail = cloudinary.uploader.upload(movie_thumbnails[i].stream,
                                                          public_id=movie_title +
                                                          "tn"+str(i+1),
                                                          folder="tcgproj3/"+movie_genre+"/"+movie_title,
                                                          resource_type="image"
                                                          )
            result_thumbnails.append(result_thumbnail['url'])

        if "watch?v=" in movie_youtubeurl:
            if "&" in movie_youtubeurl:
                cleaned_movie_youtubeurl = movie_youtubeurl.replace(
                    'watch?v=', 'embed/')
                splitted_movie_youtubeurl = cleaned_movie_youtubeurl.split(
                    '&', 1)
                uploaded__movie_youtubeurl = splitted_movie_youtubeurl[0]
            else:
                uploaded__movie_youtubeurl = movie_youtubeurl.replace(
                    'watch?v=', 'embed/')

        db.movies.insert_one({
            "name": movie_title,
            "genre": movie_genre.lower(),
            "imageurl": result_poster['url'],
            "year": movie_year,
            "maincasts": movie_maincasts.split(","),
            "synopsis": movie_synopsis,
            "directors": movie_directors.split(","),
            "youtubeurl": uploaded__movie_youtubeurl,
            'backdrop': result_backdrop['url'],
            'thumbnails': result_thumbnails
        })

        data = {'message': errors, 'error_status': 0}

        print("status code 200")

        return make_response(jsonify(data), 200)

        # flash(name + " has been added!")

        # print("/ route return post")
        # return redirect(url_for('process_landing_page'))

    else:
        # for k, v in errors.items():
        #     flash(v)
        # all_genre = db.movie_genres.find()
        # all_movies = db.movies.find()

        data = {'message': errors, 'error_status': 1}

        print("status code 400")

        return make_response(jsonify(data), 400)
        # print("/create route errors")
        # return render_template('landingpage.template.html',
        #                        all_movies=list(all_movies),
        #                        all_genre=list(all_genre),
        #                        errors=errors,
        #                        old_values=request.form)


@ app.route('/<genre>/bygenre')
def show_movieinfolist_bygenre(genre):

    movieslist = []
    dbmovieslist = []

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:

        movieslist, dbmovieslist = search_result(
            result, all_movies, movieslist, dbmovieslist)

        if not movieslist:
            flash("Sorry we found no result for {}".format(result))

            return redirect(url_for('show_landing_page'))

        else:

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

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')
    print(result)

    if result != None:

        movieslist, dbmovieslist = search_result(
            result, all_movies, movieslist, dbmovieslist)

        if not movieslist:
            flash("Sorry we found no result for {}".format(result))

            return redirect(url_for('show_landing_page'))

        else:

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


@ app.route('/<movie_id>/movieinfo')
def show_movieinfo_page(movie_id):

    dbmovieslist = []
    movieslist = []

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:
        movieslist, dbmovieslist = search_result(
            result, all_movies, movieslist, dbmovieslist)

        if not movieslist:
            flash("Sorry we found no result for {}".format(result))

            return redirect(url_for('show_landing_page'))

        else:

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


@ app.route('/<movie_id>/movieinfo', methods=['POST'])
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


@ app.route('/<movie_id>/movieinfo/update')
def show_update_movieinfo_page(movie_id):

    dbmovieslist = []
    movieslist = []

    all_genre = db.movie_genres.find()
    all_movies = db.movies.find()
    result = request.args.get('result')

    if result != None:
        movieslist, dbmovieslist = search_result(
            result, all_movies, movieslist, dbmovieslist)

        if not movieslist:
            flash("Sorry we found no result for {}".format(result))

            return redirect(url_for('show_landing_page'))

        else:

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


@ app.route('/<movie_id>/movieinfo/update', methods=['POST'])
def process_update_movieinfo_page(movie_id):

    result_thumbnails = []
    errors = validate_form(request.form)
    url = request.url
    response = requests.get(url)
    status_code = int(response.status_code)
    uploaded__movie_youtubeurl = ""

    print("Error length: {}".format(len(errors)))

    if len(errors) == 0 and status_code == 200:

        movie_title = request.form.get('name')
        movie_genre = request.form.get('genre')
        movie_imageurl = request.files['file']
        movie_year = request.form.get('year')
        movie_maincasts = request.form.get('maincasts')
        movie_synopsis = request.form.get('synopsis')
        movie_directors = request.form.get('directors')
        movie_youtubeurl = request.form.get('youtubeurl')
        movie_backdrop = request.files['backdrop']
        movie_thumbnails = request.files.getlist("thumbnails")

        movie_imageurl.seek(0)
        movie_backdrop.seek(0)

        result_poster = cloudinary.uploader.upload(movie_imageurl.stream,
                                                   public_id=movie_title+"_poster",
                                                   folder="tcgproj3/"+movie_genre+"/" + movie_title,
                                                   resource_type="image"
                                                   )

        result_backdrop = cloudinary.uploader.upload(movie_backdrop.stream,
                                                     public_id=movie_title+"_backdrop",
                                                     folder="tcgproj3/"+movie_genre+"/"+movie_title,
                                                     resource_type="image"
                                                     )
        for i in range(len(movie_thumbnails)):

            movie_thumbnails[i].seek(0)

            result_thumbnail = cloudinary.uploader.upload(movie_thumbnails[i].stream,
                                                          public_id=movie_title +
                                                          "tn"+str(i+1),
                                                          folder="tcgproj3/"+movie_genre+"/"+movie_title,
                                                          resource_type="image"
                                                          )
            result_thumbnails.append(result_thumbnail['url'])

        if "watch?v=" in movie_youtubeurl:
            if "&" in movie_youtubeurl:
                cleaned_movie_youtubeurl = movie_youtubeurl.replace(
                    'watch?v=', 'embed/')
                splitted_movie_youtubeurl = cleaned_movie_youtubeurl.split(
                    '&', 1)
                uploaded__movie_youtubeurl = splitted_movie_youtubeurl[0]
            else:
                uploaded__movie_youtubeurl = movie_youtubeurl.replace(
                    'watch?v=', 'embed/')

        db.movies.update_one({
            "_id": ObjectId(movie_id)
        }, {
            '$set': {
                "name": movie_title,
                "genre": movie_genre.lower(),
                "imageurl": result_poster['url'],
                "year": movie_year,
                "maincasts": movie_maincasts.split(","),
                "synopsis": movie_synopsis,
                "directors": movie_directors.split(","),
                "youtubeurl": uploaded__movie_youtubeurl,
                'backdrop': result_backdrop['url'],
                'thumbnails': result_thumbnails
            }
        })

        data = {'message': errors, 'error_status': 0}

        print("status code 200")

        # return redirect(url_for('show_update_movieinfo_page', movie_id=movie_id))

        return make_response(jsonify(data), 200)

        # flash(name + " has been updated!")

        # print("/<movie_id>/movieinfo/update route return post")
        # return redirect(url_for('show_update_movieinfo_page', movie_id=movie_id))

    else:

        data = {'message': errors, 'error_status': 1}

        print("status code 400")

        return make_response(jsonify(data), 400)

        # for k, v in errors.items():
        #     flash(v)

        # movie = db.movies.find_one({
        #     '_id': ObjectId(movie_id)
        # })

        # all_genre = db.movie_genres.find()
        # all_movies = db.movies.find()
        # old_values = {**movie, **request.form}

        # print("/create route errors")
        # return render_template('movieinfo.template.html',
        #                        all_movies=list(all_movies),
        #                        all_genre=list(all_genre),
        #                        errors=errors,
        #                        old_values=old_values)


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('custom404.template.html', old_values={}, errors={})


if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),
    #         port=os.environ.get('PORT'), debug=True)
    app.run(host=IP,
            port=PORT, debug=True)
