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
from models.msgcode import MsgCode
from user_util.utils import *
import json
import random

main = Blueprint('user', __name__)


@main.route('/login')
def index():
    return render_template('user/login.html')


@main.route('login', methods=['POST'])
def login():
    form = request.form
    name = form.get('username', '')
    u = User.find_one(name=name)
    if u is not None and u.validate_login(form):
        session['uid'] = u.id
        Log.log(u, '登录账号', request, '[{}] 登录系统'.format(u.name))
        if u.role == 'teacher':
            return redirect(url_for('admin.courses'))
        return redirect(url_for('index.index'))
    elif not u:
        flash('此用户未注册', 'warning')
        return redirect(url_for('user.index'))
    else:
        flash('用户名密码错误', 'warning')
        return redirect(url_for('user.index'))


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


@main.route('/register')
# @login_required
def register_page():
    return render_template('user/register.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        flash('图片验证码错误', 'warning')
        return redirect(url_for('user.register'))
    if not MsgCode.valid_code(form, use="register"):
        flash('短信验证码错误', 'warning')
        return redirect(url_for('user.register'))
    status, msgs = User.valid(form)
    if status is True:
        u = User.new(form)
        session['uid'] = u.id
        flash('注册成功', 'success')
        return redirect(url_for('user.register_success'))
    else:
        for msg in msgs:
            flash(msg, 'warning')
        return redirect(url_for('user.register'))


@main.route('/register/success')
@login_required
def register_success():
    u = current_user()
    return render_template('user/register_success.html', u=u)


@main.route('/password/forget')
def forget_password_page():
    return render_template('user/forget_password.html')


@main.route('/password/forget', methods=['POST'])
def forget_password():
    form = request.form
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        flash('图片验证码错误', 'warning')
        return redirect(url_for('user.forget_password_page'))
    if not MsgCode.valid_code(form, use="forget_password"):
        flash('短信验证码错误', 'warning')
        return redirect(url_for('user.forget_password_page'))
    if User.forget_password(form):
        flash('密码已重置', 'success')
        return redirect(url_for('index.index'))
    else:
        flash('手机号或密码格式错误', 'warning')
        return redirect(url_for('user.forget_password_page'))


@main.route('/password/update')
@login_required
def update_password_page():
    u = current_user()
    return render_template('user/update_password.html', u=u)


@main.route('/password/update', methods=['POST'])
@login_required
def update_password():
    form = request.form
    u = current_user()
    status, msgs = u.update_password(form)
    if status:
        flash('密码已重置', 'success')
        return redirect(url_for('index.index'))
    else:
        for msg in msgs:
            flash(msg, 'warning')
        return redirect(url_for('user.update_password_page'))


@main.route('/logout')
@login_required
def logout():
    p = session.pop('uid')
    flash('账号已安全退出', 'success')
    return redirect(url_for('index.index'))
