__author__ = 'nickyuan'
from enum import Enum
import re
from . import MongoModel
from . import timestamp
from flask import current_app as app
import hashlib
import os
import json

class Role(Enum):
    admin = 1
    manager = 2
    user = 3

bool_dict = {
    'true':True,
    'fasle':False,
}


class UserStatus(Enum):
    phone_checked = 1
    phone_unchecked = 2




class User(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('username', str, ''),
            ('mobile', str, ''),
            ('email', str, ''),
            ('password', str, ''),
            ('avatar', str, 'default.png'),
            ('role', str, 'user'),
            ('salt', str, 'q43129dhs*3'),
            ('status', str, 'phone_unchecked'),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        m.password = m.salted_password(form.get('password', ''))
        m.save()
        return m

    def validate_login(self, form):
        password = form.get('password', '')
        password = self.salted_password(password)
        return password == self.password

    @classmethod
    def valid(cls, form):
        mobile = form.get('mobile', '')
        password = form.get('password', '')
        repassword = form.get('repassword', '')
        valid_user = cls.find_one(mobile=mobile) is None
        valid_mobile = re.match('(^1[3|5|7|8|][\d]{9}$)|(^14[7]\d{8}$)', mobile)
        valid_password = re.match("^[\da-zA-Z]{6,20}$", password)
        vaild_repassword = password == repassword
        msgs = []
        if not valid_user:
            message = '此手机已注册'
            msgs.append(message)
        if not valid_mobile:
            message = '请输入正确格式的手机号码'
            msgs.append(message)
        if not valid_password:
            message = '请输入正确格式的密码'
            msgs.append(message)
        if not vaild_repassword:
            message = '两次输入密码不一致'
            msgs.append(message)
        status = valid_user and valid_mobile and vaild_repassword and vaild_repassword
        return status, msgs

    def update_avatar(self, avatar):
        allowed_type = ['jpg', 'jpeg', 'gif', 'png']
        oldname = avatar.filename
        if oldname != '' and oldname.split('.')[-1] in allowed_type:
            path = app.config['USER_AVATARS_DIR']
            filename = '{}_{}.png'.format(str(self.id), timestamp())
            avatar.save(path + filename)
            self.avatar = filename
        else:
            self.avatar = 'default.png'
        self.save()
        return self

    def update_dict(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.save()
        return self

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    def is_manager(self):
        return self.role == 'manager'

    def is_status_unchecked(self):
        return self.status == 'unchecked' and self.is_user()

    def is_status_checked(self):
        return self.status == 'checked' and self.is_user()

    def salted_password(self, password):
        salt = self.salt
        hash1 = hashlib.sha1(password.encode('ascii')).hexdigest()
        hash2 = hashlib.sha1((hash1 + salt).encode('ascii')).hexdigest()
        return hash2

    @staticmethod
    def validate_reset_password(form):
        password = form.get('newpassword', '')
        repassword = form.get('repassword', '')
        valid_password = re.match("^[\da-zA-Z]{6,20}$", password)
        vaild_repassword = password == repassword
        return valid_password and vaild_repassword

    def update_password(self, form):
        status = False
        msgs = []
        if self.validate_login(form) and self.validate_reset_password(form):
            password = form.get('newpassword')
            self.reset_password(password)
            status = True
        elif not self.validate_login(form):
            message = '原密码输入错误'
            msgs.append(message)
        else:
            message = '新密码输入错误'
            msgs.append(message)
        return status, msgs

    @classmethod
    def forget_password(cls, form):
        mobile = form.get('mobile')
        u = User.find_one(mobile=mobile)
        if u is not None and u.validate_reset_password(form):
            password = form.get('newpassword')
            u.reset_password(password)
            return True
        return False


    def reset_password(self, password):
        self.password = self.salted_password(password)
        self.save()
        # self.clear_token()
        return self

    def profile_pic_upload(self, pic, pic_type='credential_front'):
        allowed_type = app.config['ALLOWED_UPLOAD_TYPE']
        if pic.filename != '' and pic.filename.split('.')[-1] in allowed_type:
            filename = '{}_{}.{}'.format(self.uuid, pic_type, app.config['PRODUCT_PIC_EXT'])
            # 如果没有图片保存路径就重新创建该文件
            if not os.path.exists(app.config['PROFILE_PIC_DIR']):
                try:
                    os.mkdir(app.config['PROFILE_PIC_DIR'])
                except:
                    return False
            path = os.path.join(app.config['PROFILE_PIC_DIR'], filename)
            pic.save(path)
            return filename
        else:
            return None

    # def api_save_pic(self, files):
    #     from flask import url_for
    #     from user_util.utils import api_result
    #     status = False
    #     for k, v in files.items():
    #         # 只存一张图
    #         data = self.profile_pic_upload(pic=v, pic_type=k)
    #         if data:
    #             status = True
    #             path = url_for('static', filename='profile_pic/' + data)
    #             info = self.user_profile_info()
    #             if info:
    #                 info.save_pics(pic_type=k, filename=data)
    #             msg = '上传图片成功'
    #         else:
    #             path = ''
    #             msg = '文件不存在'
    #         return api_result(status, message=msg, data=path)

    def change_username(self, name):
        form = {"username": name}
        self.update(form)
