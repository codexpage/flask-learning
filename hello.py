from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment 
from flask_wtf import Form 
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = "hardpassword" #for wtf
app.config['SQLALCHEMY_DATABASE_URI']=\
	'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
bootstrap = Bootstrap(app)
manager=Manager(app)
moment=Moment(app)
db=SQLAlchemy(app)

@app.route("/", methods=['GET','POST'])
def hello():
	password = None
	form = NameForm()
	if form.validate_on_submit(): 
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('haha,changed name?')
		session['name'] = form.name.data
		password = form.password.data
		form.name.data = ''
		form.password.data = ''
		return redirect(url_for('hello'))
	return render_template("base.html",current_time=datetime.utcnow(),form=form,name=session.get('name'),password=password)


@app.errorhandler(404)
def page_not_found(e):
	 return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500

class NameForm(Form):
	"""Form to input name"""
	name = StringField('What is your name?', validators=[Required()])
	password = PasswordField('the password?')
	submit = SubmitField('Submit')
		



if __name__=="__main__":
	manager.run()
	