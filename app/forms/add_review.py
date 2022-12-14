from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms.validators import DataRequired, ValidationError
from wtforms import validators

class AddReview(FlaskForm):
    star_rating = IntegerField('Star Rating',validators=[DataRequired()])
    review_details = StringField('Review Details',validators=[DataRequired()])