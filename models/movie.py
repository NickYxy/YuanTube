__author__ = 'nickyuan'

from . import MongoModel
from . import timestamp
from enum import Enum
from flask import current_app as app
from flask import url_for

import os


# 评分的展示？


class Movies(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('name', str, ''),
            ('visible', str, ''),
            ('type', str, ''),
            ('status', str, ''),
            ('establishDate', str, ''),
            ('mark', str, ''),
            ('comments', str, ''),
            ('cover', str, ''),
            ('content', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def valid(cls, form):
        name = form.get('name', '')
        valid_name = cls.find_one(name=name) is None
        msgs = []
        if not valid_name:
            message = '该影片已存在'
            msgs.append(message)
        status = valid_name
        return status, msgs

    @classmethod
    def new(cls, form):
        m = super().new(form)
        return m

    def update_pic(self, pic):
        allowed_type = ['jpg', 'jpeg', 'gif', 'png']
        upload_name = pic.filename
        if upload_name != '' and upload_name.split('.')[-1] in allowed_type:
            path = app.config['MOVIE_PIC_DIR']
            ext = app.config['MOVIE_PIC_EXT']
            fullname = '{}{}.{}'.format(path, str(self.id), ext)
            pic.save(fullname)
            self.pic = '/' + fullname
            self.save()
        return self

    # def qiniu_pic(self, key='default.png'):
    #     self.pic = '{}{}{}'.format(app.config['CDN_URL'], key, '-webp')
    #     self.save()

    def set_pic_url(self, url):
        if len(url) > 0:
            self.pic = url
            self.save()

    def pic_upload(self, pic):
        allowed_type = app.config['ALLOWED_UPLOAD_TYPE']
        if pic.filename != '' and pic.filename.split('.')[-1] in allowed_type and len(self.pics) <= 20:
            filename = '{}_{}.{}'.format(self.uuid, timestamp(), app.config['MOVIE_PIC_EXT'])
            _file = '../' + app.config['MOVIE_PIC_DIR'] + filename
            _root = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(_root, _file)
            pic.save(path)
            self.pics.append(filename)
            self.save()

            return url_for('static', filename='movie_pic/' + filename)
        else:
            return False

    def pic_del(self, pic):
        self.pics.remove(pic)
        self.save()
        _file = '../' + app.config['MOVIE_PIC_DIR'] + pic
        _root = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(_root, _file)
        os.remove(path)
        return True

    @property
    def pics_url(self):
        url = [url_for('static', filename='movie_pic/' + p) for p in self.pics]
        url.reverse()
        return url
