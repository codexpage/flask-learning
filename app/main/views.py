#-*-encoding:utf-8-*-
#视图函数
from flask import render_template, session, redirect, url_for,current_app, flash, abort
from datetime import datetime
from . import main #from main(包名) import main(蓝本对象) main.route要用到
from .forms import NameForm, EditProfileAdminForm, EditProfileForm
from .. import db
from ..models import User, Role
from ..email import send_mail
from flask_login import login_required, current_user
from ..decorators import admin_required

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


@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html',user=user)
	

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash('Your profile has been updated.')
		return redirect(url_for('.user',username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html',form = form)

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user=User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash('The profile has been updated.')
		return redirect(url_for('.user',username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('edit_profile.html',form=form,user=user)




