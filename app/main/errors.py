#-*-encoding:utf-8-*-
from flask import render_template
from . import main #这里导入蓝本main

#要注册全局的错误处理程序要用errorhandler
@main.app_errorhandler(404)
def page_not_found(e):
	 return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500