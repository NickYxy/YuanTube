__author__ = 'nickyuan'
from models import *
from . import MongoModel
from . import timestamp
from enum import Enum
from flask import current_app as app
from flask import url_for

import os

# ----------------Comment----------------- #


class Comment(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('username', str, ''),
            ('userid', str, ''),
            ('comments', str, ''),
            ('comment_time', str, ''),
            ('level', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        m.password = m.salted_password(form.get('password', ''))
        m.save()
        return m