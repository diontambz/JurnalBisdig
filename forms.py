from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    doi = StringField('DOI')
    year = IntegerField('Year')
    authors = StringField('Authors')
    abstract = TextAreaField('Abstract')
    keywords = StringField('Keywords')
    submit = SubmitField('Submit')