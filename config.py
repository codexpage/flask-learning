#-*-encoding:utf-8-*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or "hardpassword" #for wtf
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	#使用邮件功能前需要export环境变量
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_ADMIN = os.environ.get('MAIL_ADMIN')
	MAIL_SERVER = 'smtp.tju.edu.cn'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	POSTS_PER_PAGE = 20

	@staticmethod
	def init_app(app):#程序配置初始化
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///'+os.path.join(basedir,'data.sqlite')

config = {
	'development' : DevelopmentConfig,
	'testing' : TestingConfig,
	'production' : ProductConfig,

	'default' : DevelopmentConfig #默认配置
}
