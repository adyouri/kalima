from flask_wtf import Form

from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SettingsForm(Form):
    email = TextField('Email', validators=[
       DataRequired(),
       Email(message="Must Provide An Actual Email :)"),
           Length(min=6, max=40)]
       )

    current_password = PasswordField('Current password', validators=[
        DataRequired()]
        )
    
    new_password = PasswordField('New password', validators=[
        DataRequired(),
        Length(min=6, max=25)]
        )

    confirm = PasswordField('Confirm your password', validators=[
        DataRequired(),
        EqualTo('new_password', message="Passwords must match")]
        )

    private_favs = BooleanField('Make my favorites private', validators = [DataRequired()])

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
