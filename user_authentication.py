# user_authentication.py

from flask_login import UserMixin
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask import flash

# Sample user data storage (you may replace this with your database code)
users = {
    'demo_user': {
        'username': 'demo_user',
        'password_hash': sha256_crypt.hash('demo_password')
    }
}

# User Model
class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def verify_password(self, password):
        if self.username in users:
            return sha256_crypt.verify(password, users[self.username]['password_hash'])
        return False

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired()])
    submit = SubmitField('Register')

# Function to register new users
def register_new_user(username, password):
    if username in users:
        return False, "Username already exists. Please choose a different username."
    users[username] = {
        'username': username,
        'password_hash': sha256_crypt.hash(password)
    }
    return True, "Registration successful. You can now log in with your new account."

