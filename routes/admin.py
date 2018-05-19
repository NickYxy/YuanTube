__author__ = 'nickyuan'
from flask import Blueprint
from routes import *
from models.user import User

main = Blueprint('admin', __name__)

# ------------------------- 用户管理 --------------------------
'''
暂时admin的功能是管理用户，包括删除、增加、修改信息、指定VIP；
另外一层是对于视频的管理，包括删除、增加、修改。
'''
