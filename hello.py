from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment 
from flask_wtf import Form 
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "hardpassword"
bootstrap = Bootstrap(app)
manager=Manager(app)
moment=Moment(app)

@app.route("/", methods=['GET','POST'])
def hello():
	name = None
	password = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		password = form.password.data
		form.name.data = ''
		form.password.data = ''
	return render_template("base.html",current_time=datetime.utcnow(),form=form,name=name,password=password)


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
	