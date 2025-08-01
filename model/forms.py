from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[
            DataRequired(message='email requred'),
            Email(message='Input correct email')
        ]
    )
    password = PasswordField(
        'password', validators=[
            DataRequired(message='password requred'),
            Length(min=5, message='Password must be at least 5 symbols')
        ]
    )
    submit = SubmitField('Enter')


class RegistrationForm(FlaskForm):
    email = StringField(
        'Email', validators=[
            DataRequired(message='email requred'),
            Email(message='Input correct email')
        ]
    )
    firstName = StringField('First name', validators=[
        DataRequired(message='First name')
    ])
    lastName = StringField('Last name', validators=[
        DataRequired(message='Last name')
    ])
    company = StringField('Company name', validators=[
        DataRequired(message='Company name')
    ])
    password = PasswordField(
        'password', validators=[
            DataRequired(message='password requred'),
            Length(min=8, message='Password must be at least 8 symbols')
        ]
    )
    submit = SubmitField('Register')
