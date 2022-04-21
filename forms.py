"""Forms for flask-feedback application"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

class AddUserForm(FlaskForm):
    """Form for adding a user"""

    username = StringField("Username: ",
                            validators=[InputRequired(message="Username is a required field"), Length(min=5, max=20, message="Unsername must be between 5 and 20 characters long")])
    password = PasswordField("Password: ",
                            validators=[InputRequired(message="Password is a required field"), Length(min=5, max=30, message="Password must be between 5 and 30 characters")])
    email = StringField("Email: ",
                        validators=[InputRequired(message="Email is a required field"), Length(max=50, message="Email may not be more than 50 characters long")])
    first_name = StringField("First Name: ",
                        validators=[InputRequired(message="First name is a required field"), Length(max=30, message="First name may not be more than 30 characters")])
    last_name = StringField("Last Name: ",
                            validators=[InputRequired(message="Last name is a required field"), Length(max=30, message="Last name may not be more than 30 characters")])


class LoginUserForm(FlaskForm):
    """Login form for user"""

    username = StringField("Username: ",
                            validators=[InputRequired(message="Username is a required field"), Length(min=5, max=20, message="Unsername must be between 5 and 20 characters long")])
    password = PasswordField("Password: ",
                            validators=[InputRequired(message="Password is a required field"), Length(min=5, max=30, message="Password must be between 5 and 30 characters")])

class AddFeedbackForm(FlaskForm):
    """Feedback form for user"""

    title = StringField("Title: ",
                        validators=[InputRequired(message="Title is a required field"), Length(min=3, max=100, message="Title must be between 3 and 100 characters")])
    content = TextAreaField("Content: ",
                        validators=[InputRequired(message="Content is a required field"), Length(min=1, message="Content must have at least 1 character to be valid")])