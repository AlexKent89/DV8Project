from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField,DateField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp, Email

class BasicForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=25, message="Fname should be between 4-25 chars")])
    address = StringField('Address', validators=[InputRequired(), Length(min=6, max=60, message="Lname should be between 6-60 chars")])
    post_code = StringField('Post_Code', validators=[InputRequired(), Length(min=4, max=10, message="Lname should be between 4-10 chars")])
    email = StringField('Email', validators=[InputRequired(), Length(min=4, max=60, message="Fname should be between 4-60 chars")])
    submit = SubmitField('Add Contact')