#-*-encoding:utf-8-*-
from flask import Blueprint

main = Blueprint('main', __name__) #构造参数 蓝本名字，蓝本所在包名

from . import views, errors #在末尾导入，防止循环导入依赖

