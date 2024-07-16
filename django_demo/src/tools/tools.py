import datetime
import hashlib
import time
import pandas as pd
import numpy as np
import after_response
from django.http import JsonResponse

from functools import wraps

from django_redis import get_redis_connection
from django.dispatch import Signal,receiver
conn = get_redis_connection('default')

my_signal = Signal()


@receiver(my_signal)
def my_signal_callback(sender, **kwargs):
    time.sleep(0.2)
    print(sender,"发送人...") # 打印Hello world!
    print(kwargs['msg']) # 打印Hello world!


@after_response.enable
def after_task(msg):
    time.sleep(0.02)
    print("after-->",msg)


def my_decorator(func):  # 函数装饰器
    def wrapper(self, request, *args, **kwargs):  # 此处增加了self
        print('自定义装饰器被调用了')
        print('请求路径%s' % request.path)
        return func(self, request, *args, **kwargs)  # 此处增加了self
    return wrapper


def iplimit(rate=2, cate=0, num=1, name=''):  # 我这里默认的是每分钟或每秒钟多少次(cate=0 秒 cate=1 分钟)
    def decorator(fn):
        @wraps(fn)
        def _wrapped(self, request, *args, **kw):

            if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
                log_ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                log_ip = request.META['REMOTE_ADDR']
            seconds = 1*num if cate == 0 else 60*num
            title = name+'_'+log_ip
            check = conn.get(title)
            if not check:
                print(check, 'check', type(check), title, seconds)
                conn.setex(title, seconds, rate)
            elif str(check) == '1':
                return JsonResponse({'code': 400, 'msg': 'you too fast,please slowly! man!'})
            else:
                conn.decr(title)
            return fn(self, request, *args, **kw)
        return _wrapped
    return decorator


class MyDecoratorMixin(object):  # 类视图装饰器
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = my_decorator(view)
        return view


def md5_password(pwd):
    hash = hashlib.md5()
    hash.update(bytes(pwd, encoding='utf-8'))
    return hash.hexdigest()


def md5_salt(pwd, salt):
    salt = salt.encode('utf-8')
    hash = hashlib.md5(salt)
    hash.update(bytes(pwd, encoding='utf-8'))
    return hash.hexdigest()


def mycode(start_no, num=1):

    if num == 1:
        xxx = conn.incr(start_no)
        no_ = start_no + str(xxx).zfill(3)
        return no_
    else:
        res = []
        for i in range(1, num+1):
            xxx = conn.incr(start_no)
            res.append(start_no + str(xxx).zfill(3))
        return res


def instance_days(year_month_day_end, year_month_day_start):
    """
    计算两个日期相差的天数
    :return:
    """
    year1, month1, day1 = year_month_day_end.split('-')
    year2, month2, day2 = year_month_day_start.split('-')

    d1 = datetime.date(int(year1), int(month1), int(day1))  # 其中year, month， day均为int类型
    d2 = datetime.date(int(year2), int(month2), int(day2))
    return (d1 - d2).days


def get_month(start_y, start_m, end_y, end_m):
    result = [start_y+'-'+start_m]
    while start_y+start_m != end_y+end_m:
        if start_m != '12':
            mm = str(int(start_m)+1)
            new = start_y+'-'+'0'+mm if len(mm) == 1 else start_y+'-'+mm
            result.append(new)
            start_y, start_m = new.split('-')
        else:
            new = str(int(start_y)+1)+'-'+'01'
            result.append(new)
            start_y, start_m = new.split('-')
    return result


def get_float_day(start,end):
    hours = (end - start).seconds / 3600/24
    days = (end-start).days
    return round(days + hours,2)


def local_save(path, data):
    try:
        with open(path, 'wb') as f:
            for content in data.chunks():
                f.write(content)

        return True, path
    except BaseException as e:
        print(e, '异常！！')
        return False, '存储异常！'


def getFlieName():
    aa = conn.get('FileUpTime')
    if not aa:
        t = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))*10
        conn.psetex("FileUpTime", 1000, t)
        return str(t)
    else:
        res = str(conn.incr('FileUpTime'))
        if str(res) == '1':
            t = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) * 10
            conn.psetex("FileUpTime", 1000, t)
            return str(t)
        return res


def get_number_id(model):
    aa = conn.get('assert_number_id')
    if not aa:
        start = 10000
        max_val = model.objects.filter(del_time=None).order_by('-number_id').first()
        if max_val:
            start = max_val.number_id + 1
        conn.set('assert_number_id', start)
        return start
    else:
        res = conn.incr('assert_number_id')
        return res


def get_days(start, end,method=1):
    if method ==1:
        if (end-start).days<2:
            return [start.strftime('%Y-%m-%d')]
        res = list(np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pd.period_range(start,end, freq='D')))
        # 开始日期，结束日期
        return res
    else:
        if end.year == start.year and end.month == start.month:
            return [start.strftime('%Y-%m')]
        return list(np.vectorize(lambda s: s.strftime('%Y-%m'))(pd.period_range(start,end, freq='M')))


def get_weeks(start_week,end_week):
    if start_week[0] == end_week[0] and start_week[1] == end_week[1]:
        return [f"{start_week[0]}-{start_week[1]}", ]
    else:
        x_s = []
        if start_week[0] == end_week[0]:
            for i in range(start_week[1], end_week[1] + 1):
                x_s.append(f"{start_week[0]}-{i}")
        else:
            end = datetime.datetime(end_week[0], 1, 1).isocalendar()
            middle = end[1]
            for i in range(start_week[1], middle + 1):
                x_s.append(f"{start_week[0]}-{i}")
            for j in range(1, end_week[1] + 1):
                x_s.append(f"{end_week[0]}-{j}")

        return x_s

def is_number(s):

    if s.count(".") == 1:  # 小数的判断

        if s[0] == "-":
            s = s[1:]

        if s[0] == ".":
            return False

        s = s.replace(".", "")

        for i in s:

            if i not in "0123456789":
                return False

        else:  # 这个else与for对应的

            return True

    elif s.count(".") == 0:  # 整数的判断

        if s[0] == "-":
            s = s[1:]

        for i in s:

            if i not in "0123456789":
                return False

        else:

            return True

    else:

        return False


class MyError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# def get_acronym(data):
#     """
#     用于提取中文的首字母
#     """
#     return "".join([i for i in lazy_pinyin(data, style=Style.FIRST_LETTER)])


# def get_first_upper(data):
#     """
#     用于提取中文的首字母
#     """
#     if len(data) > 0:
#         target = data[0]
#         aa = "".join([i for i in lazy_pinyin(target, style=Style.FIRST_LETTER)])
#         return aa.upper()
#     else:
#         return ''



if __name__ == '__main__':
    pass

    # now = datetime.datetime.now()
    # date = now + datetime.timedelta(days=-59)
    # rrr = list(np.vectorize(lambda s:
    #                            s.strftime('%Y-%m-%d'))(pd.period_range(date, now, freq='D')))
    # print(rrr)
    # print(len(rrr))

