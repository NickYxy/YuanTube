# -*- coding: utf-8 -*-
from . import MongoModel
from enum import Enum
from flask import current_app as app
import requests
import random
from config import key
import hashlib


class CodeUse(Enum):
    register = 1
    forget_password = 2


def md5_encode(string):
    m = hashlib.md5(string.encode('ascii'))
    return m.hexdigest()


class MsgCode(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('mobile', str, ''),
            ('code', str, ''),
            ('use', str, 'register'),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        vcode = str(random.randint(100000, 999999))
        m.code = vcode
        m.save()
        return m

    @classmethod
    def valid_code(cls, form, use="register"):
        mobile = form.get('mobile')
        code = form.get('msg')
        # 找到相同号码 相同用途 最新的一条
        sort = [("ct", -1)]
        msgcode = cls.find_one(mobile=mobile, use=use, __sort=sort)
        # 验证验证码是否相同，如果相同delete
        if msgcode and code == msgcode.code:
            msgcode.delete()
            return True
        return False

    def send_code(self):
        content = '您好，您的验证码是：{}【MKT】'.format(self.code)
        encode = 'UTF-8'
        values = {'username': key.msg_username,
                  'password_md5': md5_encode(key.msg_password).lower(),  # 32 位小写加密
                  'apikey': key.msg_key,
                  'mobile': '86' + self.mobile,
                  'content': content,
                  'encode': encode}
        # print(values)
        url = app.config['MSG_URL']
        r = requests.get(url, params=values)
        return r.text

    @staticmethod
    def vaild_send_mobile(form):
        from models.user import User
        use = form.get('use', 'register')
        mobile = form.get('mobile')
        u = User.find_one(mobile=mobile)
        if use == "register" and not u:
            return True
        elif use == "forget_password" and u:
            return True
        else:
            return False

    @classmethod
    def api_send_msg_code(cls, form):
        from user_util.utils import api_result
        from flask import session
        captcha = form.get('captcha', '').lower()
        if captcha != session.get('captcha', 'no captcha!'):
            status = False
            msg = "图形验证码错误"
        elif cls.vaild_send_mobile(form):
            m = cls.new(form)
            r = m.send_code()
            try:
                status, msg = r.split(':')
            except:
                status, msg = '', ''
            status = True if status == "success" else False
        else:
            status = False
            use = form.get('use', 'register')
            msg = "该手机已注册" if use == "register" else "该手机未注册"
        return api_result(status, msg)
