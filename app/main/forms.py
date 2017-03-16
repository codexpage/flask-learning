#-*-encoding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

#表单声明集合

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[Required()])
	password = PasswordField('the password?')
	submit = SubmitField('Submit')