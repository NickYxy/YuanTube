__author__ = 'nickyuan'

from user_util.utils import *
from config import config
#导入db配置
db = config.db


class ModelMixin(object):
    pass


def next_id(name):
    query = {
        'name':name
    }
    update = {
        '$inc':{
            'seq':1
        }
    }
    kwargs = {
        'query':query,
        'update':update,
        'upsert':True,
        'new':True,
    }
    doc = db['data_id']
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


