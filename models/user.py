__author__ = 'nickyuan'
from enum import Enum

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