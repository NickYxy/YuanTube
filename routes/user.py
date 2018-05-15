__author__ = 'nickyuan'
from flask import request
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import url_for
from flask import Response
from flask import session
from flask import flash
from models.user import User
from functools import wraps
from user_util.utils import *
import json
import random

main = Blueprint('user', __name__)

Model = User


@main.route('/login')
def index():
    return render_template('user/login.html')


@main.route('login', method=['POST'])
def login():
    form = request.form
    mobile = form.get('mobile', '')
    u = User.find_one(mobile=mobile)
    admin = User.find_one(username=mobile, role='admin')
    if admin and admin.validate_login(form):
        session['uid'] = admin.id
        return redirect(url_for('index.index'))
    elif u is not None and u.validate_login(form):
        session['uid'] = u.id
        return redirect(url_for('index.index'))
    elif not u and not admin:
        flash('此手机号未注册！', 'warning')
    else:
        flash('用户名密码错误！', 'warning')

        
def current_user():
    uid = int(session.get('uid', -1))
    u = User.get(uid)
    return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        # 临时禁止用户登录
        # flash('系统维护', 'danger')
        # return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_admin():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def manager_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_manager():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def clients_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_clients():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)
    return function


def finance_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_finance():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def cart_not_empty_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if not current_user().cart_not_empty():
            return redirect(url_for('index.index'))
        return f(*args, **kwargs)

    return function


def email_verify_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if not current_user().email_verified():
            flash('邮箱未验证，请先验证邮箱', 'warning')
            return redirect(url_for('user.profile'))
        return f(*args, **kwargs)

    return function


# def get_cats():
#     from models.category import Category
#     cats = Category.find(father_name='')
#     for c in cats:
#         c.sons = Category.find(father_name=c.name)
#     return cats
