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