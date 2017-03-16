#-*-encoding:utf-8-*-
from flask import render_template, current_app#记得这里要用current_app,这里app还没定义出来
from flask_mail import Message
from . import mail

#kwargs是keywords可变参数
def send_mail(to,subject,template,**kwargs):
		msg=Message(subject,sender=current_app.config['MAIL_USERNAME'],recipients=[to])
		msg.body = render_template(template + '.txt',**kwargs) #纯文本模板
		msg.html = render_template(template + '.html',**kwargs) #富文本模板
		# mail.send(msg)
		print('mail sended to '+str(to))
