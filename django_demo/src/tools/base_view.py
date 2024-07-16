#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import uuid
import coreapi
import coreschema
from django.http import QueryDict, JsonResponse
from rest_framework.request import Request
from django.db import transaction
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

from decimal import Decimal


def mydefault(d):
    """
    格式化json
    :param d:
    :return:
    """
    if isinstance(d, datetime.datetime):
        return d.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(d, datetime.date):
        return d.strftime("%Y-%m-%d")
    if isinstance(d, uuid.UUID):
        return str(d)
    if isinstance(d, Decimal):
        return float(d)


def json_res(code=200, msg="success", **kwargs):
    res = {
        "code": code,
        "msg": msg,
    }
    if kwargs:
        res.update(kwargs)
    return JsonResponse(res, json_dumps_params={'default': mydefault})


class ApiBaseView(APIView):
    """列表页基类"""
    model = None
    self_default = ''
    others = {}
    schema = AutoSchema()  # 用于接口文档必须字段的说明

    @staticmethod
    def m_others(req):
        """
        用于一些额外的查询的下拉展示数据
        :return:
        """
        return {}

    @staticmethod
    def get_kwargs(req):
        """用于自定义插入检索字段"""
        user = req.META.get('user')
        ttt = {}
        if user:
            ttt['uid'] = user['id']
        return ttt

    @staticmethod
    def get_params(req):
        """用于自定义params字段"""
        params = get_parameter_dic(req)

        return params

    def get(self, request):
        params = self.get_params(request)
        page_number = int(params.get('pageNumber', 1))
        page_size = int(params.get('pageSize', 10))
        begin = (page_number - 1) * page_size
        end = page_number * page_size
        if page_size > 100:
            return json_res(400, "pageSize不能大于100!")
        total,data = self.get_data(params, **self.get_kwargs(request))
        rows = list(data[begin:end])
        res = self.rows_desc(rows)
        self.others = self.m_others(request)
        return json_res(200, "success", data=res, total=total, others=self.others,
                        currentPage=page_number)

    def get_data(self, search, **kwargs):
        return self.model.query_by_search(search, **kwargs)


    def rows_desc(self, rows):
        """用于自定义插入字段"""
        return rows


class ApiAddView(APIView):
    """添加基类"""
    model = None
    keys = []
    key1 = []
    uniq = ''
    schema = AutoSchema()
    checked = False

    def post(self, request):
        params = get_parameter_dic(request)
        if self.checked:
            check, re_str = self.keys_check(request)
            if check:
                return json_res(403, re_str)
        if self.uniq:
            if self.model.objects.filter(**{self.uniq: params.get(self.uniq, ''), "del_time": None}):
                return json_res(402, "唯一值已存在!")
        _keys = {}
        for w in self.key1:
            val = params.get(w[0], '')
            if len(w) > 1:
                _keys.update({w[0]:val if val else w[1]})
            else:
                _keys.update({w[0]:val})

        # _keys = {i: params.get(i, '') for i in self.keys}

        sts, _keys = self.check_sth(request, _keys)
        if not sts:
            return json_res(400, _keys)
        if self.save_action(_keys):
            return json_res()
        else:
            return json_res(400, "添加失败!")

    @staticmethod
    def keys_check(req):
        # 用于检测字段类型的正确性
        return False, 'xxx格式错误！'

    @staticmethod
    def check_sth(request, data):
        # 用于添加之前操作数据或者校验数据
        return True, data

    def save_action(self, data):
        try:
            with transaction.atomic():
                self.model.objects.create(**data)
            return True
        except Exception as e:
            print(e, "save e")
            return False


def create_schema(model, need_files, other_keys=None,exclude_keys=None, add_token=True, add_id=False,add_page=False):

    files_list = []
    keys = []

    for k in need_files:
        keys.append(k[0])
        i = model._meta.get_field(k[0])
        if len(k) == 1:
            files_list.append(
                coreapi.Field(name=i.name, required=True, location="form",
                              schema=coreschema.String(description=i.verbose_name),
                              description=i.verbose_name,example=None, type="string")

                )
        else:
            files_list.append(
                coreapi.Field(name=i.name, required=False, location="form",
                              schema=coreschema.String(description=i.verbose_name),
                              description=i.verbose_name, example=k[1], type="string")

            )
    if other_keys:
        for w in other_keys:
            keys.append(w[0])
            if len(w) == 2:
                files_list.append(
                    coreapi.Field(name=w[0], required=True, location="form",
                                  schema=coreschema.String(description=w[1]),
                                  description=w[1], example=None, type="string")

                )
            else:
                files_list.append(
                    coreapi.Field(name=w[0], required=False, location="form",
                                  schema=coreschema.String(description=w[1]),
                                  description=w[1], example=w[-1], type="string")
                )
    if exclude_keys:
        for w in exclude_keys:
            if len(w) == 2:
                files_list.append(
                    coreapi.Field(name=w[0], required=True, location="form",
                                  schema=coreschema.String(description=w[1]),
                                  description=w[1], example=None, type="string")

                )
            else:
                files_list.append(
                    coreapi.Field(name=w[0], required=False, location="form",
                                  schema=coreschema.String(description=w[1]),
                                  description=w[1], example=w[-1], type="string")
                )

    if add_id:
        files_list.append(
            coreapi.Field(name="id", required=True, location="form",
                          schema=coreschema.String(description='id'),
                          description='id', example="", type="string")
        )
    if add_page:
        files_list.extend([
            coreapi.Field(name="pageNumber", required=False, location="form",
                          schema=coreschema.String(description='页码'),
                          description='页码', example=1, type="int"),
            coreapi.Field(name="pageSize", required=False, location="form",
                          schema=coreschema.String(description='pageSize'),
                          description='pageSize', example=10, type="int")])
    if add_token:
        files_list.append(
            coreapi.Field(name="AUTHORIZATION", required=False, location="header",
                          schema=coreschema.String(description='token'),
                          description='token', example=None, type="string"),

        )
    return keys, AutoSchema(manual_fields=files_list)


def create_normal_schema(target,add_token=False, add_page=False):
    files_list = []
    for w in target:
        if len(w) == 2:
            files_list.append(
                coreapi.Field(name=w[0], required=True, location="form",
                              schema=coreschema.String(description=w[1]),
                              description=w[1], example=None, type="string")
            )
        else:
            files_list.append(
                coreapi.Field(name=w[0], required=False, location="form",
                              schema=coreschema.String(description=w[1]),
                              description=w[1], example=w[-1], type="string")
            )

    if add_page:
        files_list.extend([
            coreapi.Field(name="pageNumber", required=False, location="form",
                          schema=coreschema.String(description='页码'),
                          description='页码', example=1, type="int"),
            coreapi.Field(name="pageSize", required=False, location="form",
                          schema=coreschema.String(description='pageSize'),
                          description='pageSize', example=10, type="int")])
    if add_token:
        files_list.append(
            coreapi.Field(name="AUTHORIZATION", required=False, location="header",
                          schema=coreschema.String(description='token'),
                          description='token', example=None, type="string"),

        )

    return AutoSchema(manual_fields=files_list)


class ApiEditView(APIView):
    model = None
    keys = []
    key1 = []
    uniq = ''  # 唯一字段的检查
    my_id = 'id'
    schema = AutoSchema()
    checked = False

    def post(self, request):
        params = get_parameter_dic(request)
        if self.checked:
            check, re_str = self.keys_check(request)
            if check:
                return json_res(403, re_str)
        m_id = params.get(self.my_id, '')
        data = self.model.objects.filter(**{self.my_id: m_id})
        if not data:
            return json_res(404, '参数异常！')
        if self.uniq:
            if getattr(data.first(), self.uniq) != params.get(self.uniq, ''):
                uniq_check = self.model.objects.exclude(**{self.my_id: m_id})\
                    .filter(**{self.uniq: params.get(self.uniq, '')})
                if uniq_check:
                    return json_res(402, '唯一值已存在！')
        _keys = {}
        for w in self.key1:
            val = params.get(w[0], '')
            if len(w) > 1:
                _keys.update({w[0]: val if val else w[1]})
            else:
                _keys.update({w[0]: val})

        sts, kkk = self.check_sth(request,_keys)
        if not sts:
            return json_res(400, '参数异常！')

        if self.save_action(data,kkk):
            return json_res()
        else:
            return json_res(400, '编辑失败！')

    @staticmethod
    def keys_check(req):
        # 用于检测字段类型的正确性
        return False, 'xx格式错误！'

    @staticmethod
    def check_sth(request,data):
        data.update({'update_time': datetime.datetime.now()})
        return True, data
        # 用于添加之前操作数据库

    def save_action(self, data, _keys):
        try:
            with transaction.atomic():
                data.update(**_keys)
            return True
        except Exception as e:
            print(e, "edit e")
            return False


class ApiRemoveView(APIView):
    model = None
    schema = create_normal_schema([('ids', '删除的id数组')], add_token=True)

    def post(self, request):
        params = get_parameter_dic(request)
        ids = params.get('ids', "")
        _ids = ids.split(",")
        if isinstance(_ids, str):
            _ids = eval(_ids)
        try:
            with transaction.atomic():
                self.model.objects.filter(id__in=_ids).delete()

            return JsonResponse({'code': 200, 'msg': '删除成功！'})
        except Exception as e:
            print(e, '删除异常！')
            return JsonResponse({'code': 400, 'msg': '删除异常！'})


class ApiDelView(APIView):
    model = None
    schema = create_normal_schema([('ids', '删除的id数组')], add_token=True)

    def post(self, request):
        params = get_parameter_dic(request)
        ids = params.get('ids', "")
        _ids = ids.split(",")
        if isinstance(_ids, str):
            _ids = eval(_ids)
        try:
            with transaction.atomic():
                self.model.objects.filter(id__in=_ids).update(**{'del_time':datetime.datetime.now()})

            return JsonResponse({'code': 200, 'msg': '删除成功！'})
        except Exception as e:
            print(e, '删除异常！')
            return JsonResponse({'code': 400, 'msg': '删除异常！'})


class ApiStsView(APIView):
    model = None
    schema = create_normal_schema([('status', '状态'), ('id', 'id')], add_token=True)

    def post(self, request):
        params = get_parameter_dic(request)
        sts = params.get('status', 1)
        uid = params.get('id', '')
        try:
            data = self.model.objects.filter(id=uid)
            if not data:
                return JsonResponse({'code': 400, 'msg': '数据异常！'})

            with transaction.atomic():

                data.update(**{'status': sts})

            return JsonResponse({'code': 200, 'msg': '操作成功！'})
        except Exception as e:
            print(e, '操作异常！')
            return JsonResponse({'code': 400, 'msg': '操作异常！'})


# 编写参数统一处理的方法
def get_parameter_dic(request):
    # 当用formData格式是参数在 request.data  有body  b'ids=%5B2%2C%5D'
    # 当用query 参数在query_params           有body 但是是空
    # body 时 参数在request.data
    if not isinstance(request, Request):
        return {}
    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()

    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        return query_params
    else:
        return result_data
