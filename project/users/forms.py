from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SettingsForm(FlaskForm):

    email = StringField('Email', validators=[
       Email(message="Must Provide An Actual Email :)"),
           Length(min=6, max=40)]
       )

    current_password = PasswordField('Current password')
    new_password = PasswordField('New password', validators=[
        #Length(min=6, max=25)
        ]
        )

    confirm = PasswordField('Confirm your password', validators=[
        EqualTo('new_password', message="Passwords must match")]
        )

    private_favs = BooleanField('Make my favorites private')


class RegisterForm(FlaskForm):
    username = StringField('Username', 
            validators=[DataRequired(),
                Length(min=3, max=25)]
            )

    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Must Provide An Actual Email :)"),
            Length(min=6, max=40)]
        )

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=25)]
        )

    confirm = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")]
        )
