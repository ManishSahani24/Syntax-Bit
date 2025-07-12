from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(3, 50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 50)])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(3, 50)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AskQuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Ask')    #this form will be used for asking questions