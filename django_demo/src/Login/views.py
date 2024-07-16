import datetime
import uuid
import json

import coreapi
import coreschema
from django.db import transaction
from django.http import JsonResponse
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore,  register_job

from src.Index.models import AssetInfoTable
from src.Index.models.sys import MyUsers


from django.db import transaction

from django_redis import get_redis_connection

from src.tools.base_view import create_normal_schema, get_parameter_dic, mydefault
from src.tools.tools import md5_password

conn = get_redis_connection('default')


class LoginView(APIView):
    _keys = [('account', '账号'),('password', '密码')
             ]
    schema = create_normal_schema(_keys)
    action_desc = "登录接口"
    def post(self, request):
        """
        登录
        """
        params = get_parameter_dic(request)   # vue
        account = params.get('account', '')
        password = params.get('password', '')

        check = MyUsers.objects.filter(account=account, del_time=None)
        if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
            log_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            log_ip = request.META['REMOTE_ADDR']
        print('用户的请求ip是', log_ip)
        if not check:
            return JsonResponse({'code': 401, 'msg': '帐号密码不匹配', 'data': [], })

        data = check.values('id', 'name', 'phone', 'status', 'password', 'head_img')
        user = list(data)[0]
        if user['status'] == 0:
            return JsonResponse({'code': 405, 'msg': '该账户已被管理员禁用', 'data': ''})

        db_password = user['password']
        if db_password == md5_password(password):

            token = str(uuid.uuid4()).replace('-', '')

            target = {
                'name': user['name'],
                'phone': user['phone'],
                'id': user['id'].__str__(),
            }

            conn.set(token, json.dumps(target), 60 * 60 * 24 * 1)

            with transaction.atomic():
                check.update(log_ip=log_ip, log_time=datetime.datetime.now())

            target.update({"token": token})
            return JsonResponse({'code': 200, 'msg': '登录成功！',
                                 'result': target}, json_dumps_params={'default': mydefault})
        else:
            return JsonResponse({'code': 400, 'msg': '帐号或密码错误', 'data': ''})


class LogoutView(APIView):
    _keys = [('token', 'token')

             ]
    schema = create_normal_schema(_keys)
    action_desc = "登出接口"
    def post(self, request):
        """
        登出
        """
        params = get_parameter_dic(request)
        token = params.get('token', '')
        if token:
            conn.delete(token)
        return JsonResponse({'code': 200, 'msg': '退出成功'})


IS_MAIN = 1
if IS_MAIN:
    scheduler = BackgroundScheduler()  # 创建一个调度器对象
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.remove_all_jobs()
    key = "admin_time_clock"
    try:
        # @register_job(scheduler, "interval", seconds=1)用interval方式 每1秒执行一次
        dddd = conn.get(key)
        print(dddd, 'dddd------------------------')
        if not dddd:
            conn.set(key, 1, ex=60)
            print('进入了事件........')
            @register_job(scheduler, 'cron', day_of_week='mon-sun', hour='23', minute='43', second='01', id='m_data2')
            def asset_change_sts():
                """将有截止日期的帖子变为无效状态"""
                # 定时收货
                check2 = conn.get('asset_change_lock')
                if not check2:
                    conn.set('asset_change_lock', 1, ex=72000)
                    date = datetime.datetime.now().date()
                    AssetInfoTable.objects.filter(end_date=date).update(front_sts=4)
                else:
                    print(f"帖子变为无效--遇到锁我先退出了！")


            # register_events(scheduler)
            scheduler.start()
        else:
            print('你没进去.................')

    except Exception as e:
        print(e)
        # scheduler.shutdown()









