from flask import Blueprint

# 创建蓝本，蓝本用来管理包含视图函数的文件
main = Blueprint('main', __name__)

# 引入包含视图函数的文件
from . import views, errors

from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)