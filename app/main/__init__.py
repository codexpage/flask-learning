#-*-encoding:utf-8-*-
from flask import Blueprint

main = Blueprint('main', __name__) #构造参数 蓝本名字，蓝本所在包名

from . import views, errors #在末尾导入，防止循环导入依赖

from ..models import Permission

@main.app_context_processor #Permission类加入全局上下文卡，在所有模板中都可以全局访问
def inject_perssions():
	return dict(Permission=Permission)

