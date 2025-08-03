from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from model.dbModels import UserTypeEnum


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
