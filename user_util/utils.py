__author__ = 'nickyuan'

# ------------------------- 通用配置 --------------------------
import time
import json
from uuid import uuid4

# ------------ 时间 -------------
def time_str(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(t)+ 3600 * 8))


def ymd_timestamp(s):
    return int(time.mktime(time.strptime(s, '%Y-%m-%d')))


# ------------ uuid -------------
def short_uuid():
    seed = str(uuid4())
    short_seed = seed.split('-')[-1]
    return short_seed

def api_result(success=False, message='', data=''):
    r = {
        'success': success,
        'message': message,
        'data': data,
    }
    if message:
        r['message'] = message
    if data:
        r['data'] = data
    return json.dumps(r)