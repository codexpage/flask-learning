#-*-encoding:utf-8-*-
#视图函数
from flask import render_template, session, redirect, url_for,current_app, flash
from datetime import datetime
from . import main #from main(包名) import main(蓝本对象) main.route要用到
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_mail

#路由修饰器由蓝本提供
@main.route("/", methods=['GET','POST'])
def index():
	password = None
	form = NameForm()
	if form.validate_on_submit(): 
		old_name = session.get('name')
		user =User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known']=False
			send_mail(current_app.config['MAIL_ADMIN'],'new user','mail/new_user',user=user)
		else:
			session['known']=True
		session['name']=form.name.data 
		if old_name is not None and old_name != form.name.data:
			flash('haha,changed name? mail sended')
		password = form.password.data
		form.name.data = ''
		form.password.data = ''
		return redirect(url_for('.index'))#注意这里路由写法是main.hello的缩写，这里的index是index()路由函数的名字，蓝本名字相当于命名空间
	return render_template("index.html",current_time=datetime.utcnow(),form=form,name=session.get('name'),password=password,known=session.get('known',False))
