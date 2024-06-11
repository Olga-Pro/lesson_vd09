from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User
from flask import flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

class RegistrationForm (FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято')

    def validate_email(self, email):
        control = User.query.filter_by(email=email.data).first()
        if control:
            raise ValidationError('Эта почта уже используется')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[Optional(), Length(min=3, max=35)])
    email = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('New Password', validators=[Optional()])
    confirm_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('password')])
    submit = SubmitField('Update')

    def __init__(self):
        super(EditProfileForm, self).__init__()
        self.current_username = current_user.username
        self.current_email = current_user.email
    def validate_username(self, username):
        if username.data and username.data != self.current_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя уже занято')

    def validate_email(self, email):
        if email.data and email.data != self.current_email:
            control = User.query.filter_by(email=email.data).first()
            if control:
                raise ValidationError('Эта почта уже используется')


