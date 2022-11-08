from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField
from wtforms import validators


class ChangeInventory(FlaskForm):
    change_in_quantity = IntegerField('change_in_quantity')
    absolute_quantity = IntegerField('absolute_quantity')
    description = StringField('description',validators=[DataRequired()])