import json
import time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

conn = get_redis_connection('default')


class MyMiddle(MiddlewareMixin):
    """
    自定义中间件：用来验证token
    """
    pass_list = ['login', 'api-auth', 'docs', "admin", "media",
                 ]

    def process_request(self, request):
        request.start_time = time.time()
        check = [True if i not in request.path else False for i in self.pass_list]
        if all(check):
            token = request.META.get('HTTP_AUTHORIZATION', '')
            if token:
                if token.startswith('Bearer'):
                    token = token.split(' ')[1]
                try:
                    user = json.loads(conn.get(token))
                    if user:
                        request.META["user"] = user
                except:
                    return JsonResponse({"code": 1000, "msg": "token失效"})
            else:
                return JsonResponse({"code": 404, "msg": "未携带token！"})

    def process_response(self, request, response):  # 上线后不想看了就删了这个函数吧
        """计算响应时间"""
        execute_time = time.time() - request.start_time
        path = request.get_full_path()
        print('路径：%s,响应时间为：%s' % (path, execute_time))
        return response

