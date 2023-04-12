"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from app.models import Movies
from app.forms import MovieForm
import datetime

###
# Routing for your application.
###

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            
            title = form.title.data
            poster = form.poster.data
            poster_name = secure_filename(poster.filename)
            description = form.description.data

            current_time= datetime.datetime.now()            
            response = {
                "message": "Movie Successfully added",
                "title": title,
                "poster": poster.filename,
                "description": description
            }

            poster.save(os.path.join(app.config['UPLOAD_FOLDER'],poster_name))

            movie_info = Movies(title,description,poster_name,current_time)
            db.session.add(movie_info)
            db.session.commit()
            return jsonify(data=response)

        errors = form_errors(form)
        response = {'errors': errors}
        return jsonify(error=response)

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/movies', methods=['GET'])
def getallmovies():
    movies = Movies.query.all()
    movies_list = []
    for movie in movies:
        movie_dict = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': url_for('get_image', filename=movie.poster, _external=True)
        }
        movies_list.append(movie_dict)
    response = {'movies': movies_list}
    return jsonify(response)

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404