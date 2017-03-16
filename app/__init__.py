#-*-encoding:utf-8-*-
from flask import Flask

from flask_bootstrap import Bootstrap
from flask_moment import Moment 
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config

#这些类必须写在函数外面，这样包内模块才能import
bootstrap = Bootstrap()
moment=Moment()
mail = Mail()
db=SQLAlchemy()

def create_app(config_name): #app工厂函数
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	#初始化其他类
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	#路由和自定义错误页面
	from .main import main as main_blueprint #导入子包中的蓝本
	app.register_blueprint(main_blueprint) #注册蓝本
	return app