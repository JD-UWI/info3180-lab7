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
from app.models import Movies
from app.forms import MovieForm

###
# Routing for your application.
###
rootdir = os.getcwd()

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['GET','POST'])
def movies():
    form = MovieForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(form_errors(form))
            return redirect((url_for('index')))
        else:
            title = form.title.data
            description = form.description.data
            poster = form.photo.data
            poster_name= secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD'], poster_name))

            movie_info = Movies(title, description, poster, created_at)
            db.session.add(movie_info)
            db.session.commit()
            return redirect(url_for('index')) # Update this to redirect the user to a route that displays all uploaded image files

    return jsonify(message="Movie successfully added",
                   title=f"{title}",
                   poster=f"{poster}",
                   description=f"{description}")
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