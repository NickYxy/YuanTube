__author__ = 'nickyuan'
import time


def time_str(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(t) + 3600 * 8))


def pay_status(t):
    d = {
        0: '<span class="text-danger">未支付</span>',
        1: '<span class="text-success">已支付</span>',
    }
    return d.get(t, '待处理')


def bill_mode(t):
    d = {
        0: '金额',
        1: '点数',
    }
    return d.get(t, '待处理')


def buy_status(status):
    r = '已购' if status else '未购'
    return r


def user_role(role):
    d = {
        'admin': '管理员',
        'manager': '客户经理',
        'client': '自然人',
        'company': '机构',
    }
    return d.get(role, '自然人')


def user_status(status):
    d = {
        'register': '新注册',
        'unsubmit': '未提交',
        'unchecked': '未审核',
        'checked': '已审核',
        'refused': '驳回申请',
    }
    return d.get(status, '新注册')


def question_type(question):
    d = {
        'single': '单选题',
        'multiple': '多选题',
        'judge': '判断题',
        'comprehensive': '综合题'
    }
    return d.get(question, '单选题')


def question_status(question):
    d = {
        'enabled': '启用',
        'cancelled': '废弃',
    }
    return d.get(question, '启用')


def exam_status(exam):
    d = {
        'unpublished': '未发布',
        'published': '已发布',
    }
    return d.get(exam, '未发布')


def course_status(course):
    d = {
        'invisible': '不可见',
        'visible': '可见',
    }
    return d.get(course, '不可见')


filters = {
    'time_str': time_str,
    'pay_status': pay_status,
    'bill_mode': bill_mode,
    'buy_status': buy_status,
    'user_role': user_role,
    'user_status': user_status,
    'question_type': question_type,
    'question_status': question_status,
    'exam_status': exam_status,
    'course_status': course_status,
}
