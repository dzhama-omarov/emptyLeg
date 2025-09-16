"""Form definitions used by the Flask application.

This module contains WTForms form classes for user authentication and
registration used in server-side rendered templates.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from model.dbModels import UserTypeEnum


class LoginForm(FlaskForm):
    """Form for user authentication (email and password)."""
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
    """Form for new user registration with validation."""
    firstName = StringField('First name', validators=[
        DataRequired(message='First name')
    ])
    lastName = StringField('Last name', validators=[
        DataRequired(message='Last name')
    ])
    company = StringField('Company name', validators=[
        DataRequired(message='Company name')
    ])
    email = StringField(
        'Email', validators=[
            DataRequired(message='email requred'),
            Email(message='Input correct email')
        ]
    )
    userType = SelectField(
        'Account Type',
        choices=[(e.name, e.value) for e in UserTypeEnum],
        validators=[DataRequired()]
    )
    password = PasswordField(
        'password', validators=[
            DataRequired(message='password requred'),
            Length(min=8, message='Password must be at least 8 symbols')
        ]
    )
    confirmPassword = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Register')
