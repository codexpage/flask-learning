#-*-encoding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User, Role

#表单声明集合

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[Required()])
	password = PasswordField('the password?')
	submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
	name = StringField('Name', validators=[Length(0,64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
	email = StringField('Email', validators=[Email(),Required(),Length(1,64)])
	username = StringField('Username', validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must only have letters, numbers, dots and underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role',coerce=int)
	name = StringField('Real Name',validators=[Length(0,64)])
	location = StringField('Location',validators=[Length(0,64)])
	about_me = TextAreaField('About Me')
	submit = SubmitField('Submit')

	def __init__(self,user,*args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self,field):
		if field.data != self.user.email and \
			User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self,field):
		if field.data != self.user.username and \
			User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')


class PostForm(FlaskForm):
	body = TextAreaField("What's on your mind?", validators=[Required()])
	submit = SubmitField('Submit')




