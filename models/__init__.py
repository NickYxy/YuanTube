__author__ = 'nickyuan'


from config import config
#导入db配置
db = config.db


def timestamp():
    return int(time.time)
