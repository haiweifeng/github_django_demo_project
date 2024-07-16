import datetime
import re

from django.db import transaction
from rest_framework.views import APIView
from src.tools.tools import after_task
from src.Index.models import AssetInfoTable
from src.tools.base_view import ApiBaseView, create_schema, json_res, get_parameter_dic, ApiAddView, ApiEditView, \
    create_normal_schema


class AssetListView(ApiBaseView):
    """
    帖子列表页
    """
    model = AssetInfoTable
    action_desc = "帖子列表"
    key1 = [("title", ""), ("desc", ""), ("user_name", ""), ("user_phone", ""),
            ("number_id", 0), ("company_name", ""),
            ("front_sts", 0), ("source", 0),
            ("value", 0), ("accept_man_id", ""), ("c1", ""), ("c2", ""), ("sheng_id", ""),
            ("shi_id", ""), ("zone_id", ""), ("power_sts", 0)
            ]
    key2 = [("start_time","开始时间",""),("end_time","结束时间","")]
    _, schema = create_schema(model, key1, key2, add_page=True)

    def post(self, request):
        params = self.get_params(request)
        page_number = int(params.get('pageNumber', 1))
        page_size = int(params.get('pageSize', 10))
        begin = (page_number - 1) * page_size
        end = page_number * page_size
        if page_size > 100:
            return json_res(400, "pageSize不能大于100!")
        t,other, data = self.get_data(params, **self.get_kwargs(request))
        rows = list(data[begin:end])
        res = self.rows_desc(rows)
        info = {"total":0,"power":0,"pub":0,"delete":0}
        for w in other:
            num = w.get('nums',0)
            info['total'] += num
            if w['power_sts'] == 2:
                info.update({"power": num})
            if w['power_sts'] == 3:
                info.update({"pub":num})
            if w['power_sts'] == 4:
                info.update({"delete": num})
        return json_res(200, "success", data=res, total=t, others=info,
                        currentPage=page_number)
    def get_data(self, search, **kwargs):
        t,a, b = self.model.query_by_search(search, **kwargs)
        return t,a, b


class AssetAddView(ApiAddView):
    """
       添加帖子
    """
    model = AssetInfoTable
    action_desc = "帖子添加"
    key1 = [('title',), ('desc',), ('user_name',), ('user_phone',),
            ("sheng_id",), ("shi_id",), ("zone_id", ""), ("c1",), ("c2",), ("vol",),("cycle",1),
            ("unit", ""), ("images", ""), ("key_words", ""), ("value", 1),
            ("valuation", 1), ("company_name", ""),
            ("com_sheng_id", ""), ("com_shi_id", ""), ("com_zone_id", ""), ("com_address", ""),
            ("industry_id", ""), ("remark", ""),("industry", ""),("front_sts",2),("source",1)
            ]
    keys, schema = create_schema(model, key1)

    @staticmethod
    def keys_check(req):
        # 用于检测字段类型的正确性
        if not req.data.get('title', ''):
            return True, '标题不可为空！'
        if not re.match(r"^1[3456789]\d{9}$", req.data.get('user_phone', '')):
            return True, '手机号格式错误！'
        return False, 'success'

    @staticmethod
    def check_sth(request, data):
        user = request.META.get('user')
        now = datetime.datetime.now()

        week = now.isocalendar()
        middle = {"power_sts": 3, "accept_man_id": user['id'],
                  "accept_man_name": user['name'],
                  "accept_time": now, "week":f"{week[0]}-{week[1]}",
                  "end_date": now.date()+datetime.timedelta(days=30), "add_time": now}
        data.update(middle)
        return True, data


class AssetEditView(ApiEditView):
    """
        编辑发布帖子
    """
    model = AssetInfoTable

    action_desc = "帖子编辑"
    key1 = [('title',), ('desc',), ('user_name',), ('user_phone',),
            ("sheng_id",), ("shi_id",), ("zone_id", ""), ("c1",), ("c2",), ("vol",),("cycle",1),
            ("unit", ""), ("images", ""),  ("key_words", ""), ("value", 1),
            ("valuation", 1), ("company_name", ""),
            ("com_sheng_id", ""), ("com_shi_id", ""), ("com_zone_id", ""), ("com_address", ""),
            ("industry", ""), ("industry_id", ""), ("remark", ""),("front_sts",2),("source",6)
            ]
    keys, schema = create_schema(model, key1, add_id=True)

    @staticmethod
    def keys_check(req):
        # 用于检测字段类型的正确性
        if not req.data.get('title', ''):
            return True, '标题不可为空！'
        if not re.match(r"^1[3456789]\d{9}$", req.data.get('user_phone', '')):
            return True, '手机号格式错误！'
        return False, 'success'

    @staticmethod
    def check_sth(request, data):
        now = datetime.datetime.now()
        data.update({'update_time': now})
        middle = {"power_sts": 3,
                  "end_date": now.date() + datetime.timedelta(days=30)}
        data.update(middle)

        return True, data
        # 用于添加之前操作数据库


class AssetEditGetNextView(APIView):
    """帖子-编辑获取下一条----用于连续编辑"""
    model = AssetInfoTable
    action_desc = "帖子编辑获取下一条"
    key1 = [("title", ""), ("desc", ""), ("user_name", ""), ("user_phone", ""),
            ("number_id", 0), ("company_name", ""),
            ("front_sts", 0), ("source", 0),
            ("value", 0), ("accept_man_id", ""), ("c1", ""), ("c2", ""), ("sheng_id", ""),
            ("shi_id", ""), ("zone_id", ""), ("power_sts", 0)
            ]
    key2 = [("start_time", "开始时间", ""), ("end_time", "结束时间", ""),
            ("position", "当前位置", 0), ("is_next", "只获取下一条", 1)]
    _, schema = create_schema(model, key1, key2,add_page=True)

    def post(self, request):
        params = get_parameter_dic(request)
        page_size = int(params.get('pageSize', 10))
        if page_size > 100:
            return json_res(400, "pageSize不能大于100!")
        _,sts, data = self.model.query_by_search(params)
        if sts == -1:
            return json_res(400, msg='已经是最后一条了！')
        elif sts == -2:
            return json_res(400, msg='已经是第一条了！')
        else:
            res = list(data)[0]
            return json_res(200, "success", data=res)


class DemoBaseTestView(APIView):
    action_desc = "一个用于测试的接口"
    _keys = [('vip_id', '会员id'),]
    schema = create_normal_schema(_keys)
    def post(self, request):
        vip_id = request.data.get('vip_id', '')
        print("vip",vip_id)
        after_task.after_response(vip_id)
        # my_signal.send(sender=vip_id, msg='Hello world')
        return json_res(code=200, msg=vip_id)