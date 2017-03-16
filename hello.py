#-*-encoding:utf-8-*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager, Shell
from flask_moment import Moment 
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail,Message

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = "hardpassword" #for wtf
app.config['SQLALCHEMY_DATABASE_URI']=\
	'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.tju.edu.cn'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#使用邮件功能前需要export环境变量
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_ADMIN'] = os.environ.get('MAIL_ADMIN')


bootstrap = Bootstrap(app)
manager=Manager(app)
moment=Moment(app)
db=SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)


manager.add_command('db',MigrateCommand) #加上db命令表示migrate


@app.route("/", methods=['GET','POST'])
def hello():
	password = None
	form = NameForm()
	if form.validate_on_submit(): 
		old_name = session.get('name')
		user =User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known']=False
		else:
			session['known']=True
		session['name']=form.name.data 
		if old_name is not None and old_name != form.name.data:
			flash('haha,changed name? mail sended')
			send_mail(app.config['MAIL_ADMIN'],'new user','mail/new_user',user=user)
		password = form.password.data
		form.name.data = ''
		form.password.data = ''
		return redirect(url_for('hello'))
	return render_template("index.html",current_time=datetime.utcnow(),form=form,name=session.get('name'),password=password,known=session.get('known',False))


@app.errorhandler(404)
def page_not_found(e):
	 return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500

class NameForm(FlaskForm):
	"""Form to input name"""
	name = StringField('What is your name?', validators=[Required()])
	password = PasswordField('the password?')
	submit = SubmitField('Submit')
		
class Role(db.Model):
	"""Role model"""
	__tablename__='roles'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship('User',backref='role',lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context = make_shell_context))

#kwargs是keywords可变参数
def send_mail(to,subject,template,**kwargs):
		msg=Message(subject,sender=app.config['MAIL_USERNAME'],recipients=[to])
		msg.body = render_template(template + '.txt',**kwargs) #纯文本模板
		msg.html = render_template(template + '.html',**kwargs) #富文本模板
		# mail.send(msg)
		print('mail sended to '+to)


if __name__=="__main__":
	manager.run()
	