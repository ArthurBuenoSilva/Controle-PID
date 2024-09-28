from flask_wtf import FlaskForm
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired


class DatasetForm(FlaskForm):
    dataset = FileField("dataset", validators=[DataRequired()])
