__author__ = 'nickyuan'

from . import MongoModel
from . import timestamp
from enum import Enum
from flask import current_app as app
from flask import url_for

import os


class MovieCategory(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('name', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def valid(cls, form):
        name = form.get('name', '')
        valid_name = cls.find_one(name=name) is None
        msgs = []
        if not valid_name:
            message = '该分类已存在'
            msgs.append(message)
        status = valid_name
        return status, msgs

    @classmethod
    def new(cls, form):
        m = super().new(form)
        return m

    @classmethod
    def count(self, uuid):
        c = MovieCategory.get_uuid(uuid)
        ms = Movies.all()
        l = 0
        # print(c)
        for m in ms:
            if m.category == c.name:
                l += 1
        return l


class Category(Enum):
    剧情 = 1
    喜剧 = 2
    动作 = 3
    爱情 = 4
    科幻 = 5
    动画 = 6
    悬疑惊悚恐怖 = 7
    纪录片 = 8
    音乐 = 9
    家庭 = 10
    儿童 = 11
    历史战争 = 12
    奇幻冒险 = 13
    灾难 = 14
    武侠 = 15


# 评分的展示？


class Movies(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('name', str, ''),
            ('category', str, ''),
            ('actor', list, []),
            ('category_uuid', str, ''),
            ('visible', str, ''),
            ('type', str, ''),
            ('status', str, 'invisible'),
            ('establishDate', int, 0),
            ('mark', str, ''),
            ('comments', str, ''),
            ('cover', str, ''),
            ('content', str, ''),
            ('country', str, ''),
            ('uploadTime', int, 0),
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
    def new(cls, form, **kwargs):
        m = super().new(form, **kwargs)
        m.category_uuid = MovieCategory.find_one(name=m.category).uuid
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

    def pic_upload(self, pic):
        allowed_type = app.config['ALLOWED_UPLOAD_TYPE']
        if pic is not None and pic.filename != '' and pic.filename.split('.')[-1] in allowed_type:
            filename = '{}_{}.{}'.format(self.uuid, timestamp(), app.config['PRODUCT_PIC_EXT'])
            _file = '../' + app.config['MOVIE_PIC_DIR'] + filename
            _root = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(_root, _file)
            pic.save(path)
            self.pics = filename
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
