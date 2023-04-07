
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

# Add any form classes for Flask-WTF here
class MovieForm(FlaskForm):
    title = StringField('Title',validators=[InputRequired()])
    description = TextAreaField('Description',validators=[InputRequired(), Length(max=200)])
    poster = FileField('Poster',validators=[FileRequired(), FileAllowed(['jpg','png'], 'Images only!')])
    #submit = SubmitField('Send')