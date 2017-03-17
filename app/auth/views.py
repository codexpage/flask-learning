#-*-encoding:utf-8-*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth

from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm, PasswordResetRequestForm

from .. import db
from ..email import send_mail

@auth.before_app_request #在全局的所有request之前，判断如果1.用户登录2.且未确认3.且请求的端点不在auth蓝本中,则强制跳转到unconfirm界面
def before_request():
	if current_user.is_authenticated \
			and not current_user.confirmed \
			and request.endpoint \
			and request.endpoint[:5]!= 'auth.'\
			and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
			username=form.username.data,
			password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_mail(user.email, 'Cofirm Your Account', 'auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email.')
		return redirect(url_for('auth.login'))#or main.index

	return render_template('auth/register.html',form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirmed')#重发确认邮件
@login_required
def resend_confirmation(): 
	token = current_user.generate_confirmation_token()
	send_mail(current_user.email, 'Confirm Your Account',
		'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been send to you by email.')
	return redirect(url_for('main.index'))

@auth.route('/change-password',methods=['GET','POST'])
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			flash('Your Password has been updated')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid Password')
	return render_template('auth/change_password.html',form=form)


@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
	form = PasswordResetRequestForm()
	if not current_user.is_anonymous: #reset密码时必须没有登录
		return redirect(url_for('main.index'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_mail(user.email,'Reset Your Password','auth/email/reset_password',user=user,token=token,next=request.args.get('next'))
			flash('An email with instruction to reset your password is send to you.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html',form=form)


@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
	form = PasswordResetForm()
	if not current_user.is_anonymous: #reset密码时必须没有登录
		return redirect(url_for('main.index'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.password.data):
			flash('Your password has been updated.')
			return redirect(url_for('auth.login'))
		else:
			flash('update fail')
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html',form=form)



