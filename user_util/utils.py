import time
from uuid import uuid4
import json
import os
from datetime import datetime


def timestamp():
    return int(time.time())


def time_str(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(t) + 3600 * 8))


def ymd_timestamp(s):
    return int(time.mktime(time.strptime(s, '%Y-%m-%d')))


def short_uuid():
    seed = str(uuid4())
    short_seed = seed.split('-')[-1]
    return short_seed


def safe_list_get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default


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


def get_page(total, p):
    show_page = 5  # 显示的页码数
    pageoffset = 2  # 偏移量
    start = 1  # 分页条开始
    end = total  # 分页条结束

    if total > show_page:
        if p > pageoffset:
            start = p - pageoffset
            if total > p + pageoffset:
                end = p + pageoffset
            else:
                end = total
        else:
            start = 1
            if total > show_page:
                end = show_page
            else:
                end = total
        if p + pageoffset > total:
            start = start - (p + pageoffset - end)

    # 用于模版中循环
    dic = range(start, end + 1)
    return dic


def project_path():
    utils_file = os.path.realpath(__file__)
    utils_dir = os.path.dirname(utils_file)
    root = os.path.join(utils_dir, os.pardir)
    return root


def log_path():
    root = project_path()
    path = os.path.join(root, 'log.txt')
    return path


def current_datetime():
    pattern = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    now = now.strftime(pattern)
    return now


def log(*args, **kwargs):
    file = log_path()
    prompt = '>>>'
    formatted_datetime = current_datetime()

    # a -> open for writing, appending to the end of the file if it exists
    with open(file, mode='a', encoding='utf-8') as f:
        print(prompt, formatted_datetime, *args, **kwargs)
        print(prompt, formatted_datetime, file=f, *args, **kwargs)


# 目的是过滤 搜索表单 中某些搜索字段为空的情况
def empty_field_filter(d):
    new_d = {}
    for k, v in d.items():
        if len(v) > 0:
            new_d[k] = v
    return new_d
