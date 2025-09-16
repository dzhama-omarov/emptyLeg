"""Authentication-related WTForms used in auth templates.

Contains `RegistrationForm` and `LoginForm` with field-level
validation for password strength and email formatting.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError
)
import re


class RegistrationForm(FlaskForm):
    """Registration form with basic password strength validation."""
    company = StringField(
        'Company Name',
        validators=[
            DataRequired(message='Company name is required'),
            Length(
                min=2,
                max=100,
                message='Company name must be between 2 and 100 characters',
            ),
        ],
    )

    full_name = StringField(
        'Full Name',
        validators=[
            DataRequired(message='Full name is required'),
            Length(
                min=2,
                max=100,
                message='Full name must be between 2 and 100 characters',
            ),
        ],
    )

    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email is too long')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        """Ensure the password contains at least one letter and one number."""
        if password.data:
            if not re.search(r'[A-Za-z]', password.data):
                raise ValidationError(
                    'Password must contain at least one letter'
                )
            if not re.search(r'\d', password.data):
                raise ValidationError(
                    'Password must contain at least one number'
                )


class LoginForm(FlaskForm):
    """Simple login form with optional remember-me flag."""
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Log In')
