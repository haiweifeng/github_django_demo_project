#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import time
import uuid

from django.db import models


class MyRoles(models.Model):
    """角色表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, verbose_name='角色名称', default='',null=True,blank=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    del_time = models.DateTimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间',db_index=True)

    class Meta:
        verbose_name = verbose_name_plural = '角色表'
        db_table = 'my_roles'

    @staticmethod
    def query_by_search(search, **kwargs):
        result = MyRoles.objects.filter(del_time=None)

        if 'name' in search and search['name']:
            result = result.filter(name__contains=search['name'])
        if 'start_time' in search and search['start_time']:
            startTime = datetime.datetime.strptime(search['start_time'], '%Y-%m-%d')
            result = result.filter(created_time__gte=startTime)
        if 'end_time' in search and search['end_time']:
            endTime = datetime.datetime.strptime(search['end_time'], '%Y-%m-%d') + datetime.timedelta(days=1)
            result = result.filter(created_time__lt=endTime)
        total = result.count()
        return total, result.order_by('-created_time').values()


class MyUsers(models.Model):

    """用户表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number_id = models.CharField(default="", max_length=64, verbose_name='数字id', null=True, blank=True)
    account = models.CharField(max_length=128, verbose_name='账号', default='',null=True,blank=True)
    name = models.CharField(max_length=128, verbose_name='用户姓名', default='',null=True,blank=True)
    head_img = models.CharField(max_length=128, verbose_name='头像', default='',null=True,blank=True)
    phone = models.CharField(max_length=16, verbose_name='手机号', default='',null=True,blank=True)
    password = models.CharField(max_length=64, verbose_name='密码', default='',null=True,blank=True)

    log_ip = models.CharField(max_length=64, verbose_name='登陆ip', default='',null=True,blank=True)
    log_time = models.DateTimeField(verbose_name='登陆时间', null=True, blank=True)

    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    del_time = models.DateTimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间',db_index=True)

    class Meta:
        verbose_name = verbose_name_plural = '用户表'
        db_table = 'my_users'

    @staticmethod
    def query_by_search(search, **kwargs):
        result = MyUsers.objects.filter(del_time=None)
        if 'phone' in search and search['phone']:
            result = result.filter(phone__contains=search['phone'])
        if 'name' in search:
            result = result.filter(name__contains=search['name'])
        return result.count(),result.order_by('-created_time').values()


class NumberRoles(models.Model):
    """测试数字id角色表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=64, verbose_name='角色名称', default='',null=True,blank=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    del_time = models.DateTimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间',db_index=True)

    class Meta:
        verbose_name = verbose_name_plural = '测试数字id角色表'
        db_table = 'number_roles'

    @staticmethod
    def query_by_search(search, **kwargs):
        result = NumberRoles.objects.filter(del_time=None)

        if 'name' in search and search['name']:
            result = result.filter(name__contains=search['name'])
        if 'start_time' in search and search['start_time']:
            startTime = datetime.datetime.strptime(search['start_time'], '%Y-%m-%d')
            result = result.filter(created_time__gte=startTime)
        if 'end_time' in search and search['end_time']:
            endTime = datetime.datetime.strptime(search['end_time'], '%Y-%m-%d') + datetime.timedelta(days=1)
            result = result.filter(created_time__lt=endTime)
        total = result.count()
        return total, result.order_by('-created_time').values()