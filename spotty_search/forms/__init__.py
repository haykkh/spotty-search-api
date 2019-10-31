from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    artist = StringField('Artist')
    album = StringField('Album')
    track = StringField('Track')