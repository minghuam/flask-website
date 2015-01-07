from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

class LoginForm(Form):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class NewPostForm(Form):
	title = StringField('Title', validators=[Required()])
	body = TextAreaField('Body', validators=[Required()])
	submit = SubmitField('Submit')
	preview = SubmitField('Preview')