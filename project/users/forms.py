from flask_wtf import Form

from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from flask_login import current_user
from project import app

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SettingsForm(Form):

    email = TextField('Email', validators=[
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


class RegisterForm(Form):
    username = TextField('Username', 
            validators=[DataRequired(),
                Length(min=3, max=25)]
            )

    email = TextField('Email', validators=[
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
