#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import uuid
import pandas as pd
from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncMonth


class AssetInfoTable(models.Model):
    """帖子表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128, verbose_name='帖子标题', default='', null=True, blank=True)
    desc = models.TextField(verbose_name='帖子描述', default='', null=True, blank=True)
    user_name = models.TextField(verbose_name='联系人', null=True, blank=True, default="")
    user_phone = models.TextField(verbose_name='电话', null=True, blank=True, default="")
    source = models.PositiveIntegerField(default=0, verbose_name='来源类型', null=True, blank=True)
    front_sts = models.PositiveIntegerField(default=1, verbose_name='前台状态', null=True, blank=True)
    cycle = models.PositiveIntegerField(default=1, verbose_name='周期', null=True, blank=True)
    source_record_id = models.CharField(default="", max_length=64, verbose_name='各种来源的记录id', null=True, blank=True)
    accept_man_id = models.CharField(default="", max_length=64, verbose_name='申领人id', null=True, blank=True)
    accept_man_name = models.CharField(default="", max_length=64, verbose_name='申领人name', null=True, blank=True)
    accept_time = models.DateTimeField(default=None,null=True,blank=True, verbose_name='申领时间')
    number_id = models.CharField(default="",max_length=64, verbose_name='数字id', null=True, blank=True, db_index=True)
    power_sts = models.PositiveIntegerField(default=1, verbose_name='状态', null=True, blank=True)
    sheng_id = models.CharField(default="", max_length=64, verbose_name='省ID', null=True, blank=True, db_index=True)
    shi_id = models.CharField(default="", max_length=64, verbose_name='市ID', null=True, blank=True, db_index=True)
    zone_id = models.CharField(verbose_name='区id', null=True, blank=True, max_length=64, default="")
    address = models.CharField(verbose_name='地址', null=True, blank=True, max_length=128, default="")
    week = models.CharField(verbose_name='周', null=True, blank=True, max_length=64, default="")

    cate_name = models.CharField(verbose_name='分类全称', null=True, blank=True, max_length=128, default="")
    c1 = models.CharField(verbose_name='类别1', null=True, blank=True, max_length=64, default="")
    c2 = models.CharField(verbose_name='类别2', null=True, blank=True, max_length=64, default="")
    c3 = models.CharField(verbose_name='类别3', null=True, blank=True, max_length=64, default="")
    vol = models.CharField(max_length=64, verbose_name='处置量', default='', null=True, blank=True)
    unit = models.CharField(max_length=64, verbose_name='单位', default='', null=True, blank=True)
    images = models.TextField(verbose_name='图片数组-前端转为json字符串', default='', null=True, blank=True)
    video_url = models.TextField(verbose_name='视频url', default='', null=True, blank=True)
    key_words = models.TextField(verbose_name='关键词', default='', null=True, blank=True)
    labels = models.TextField(verbose_name='标签', default='', null=True, blank=True)
    value = models.PositiveIntegerField(default=0, verbose_name='价值判定', null=True, blank=True)
    valuation = models.PositiveIntegerField(default=8, verbose_name='估值', null=True, blank=True)
    company_name = models.CharField(verbose_name='公司名称', null=True, blank=True, max_length=128, default="")
    com_sheng_id = models.CharField(default="", max_length=64, verbose_name='省ID', null=True, blank=True)
    com_shi_id = models.CharField(default="", max_length=64, verbose_name='市ID', null=True, blank=True)
    com_zone_id = models.CharField(verbose_name='区id', null=True, blank=True, max_length=64, default="")
    com_address = models.CharField(verbose_name='地址', null=True, blank=True, max_length=64, default="")
    industry = models.CharField(verbose_name='所属行业', null=True, blank=True, max_length=64, default="")
    industry_id = models.PositiveIntegerField(default=0, verbose_name='行业id', null=True, blank=True)
    remark = models.TextField(verbose_name='备注', default='', null=True, blank=True)
    end_date = models.DateField(default=None,null=True,blank=True, verbose_name='有效截止日期')
    add_time = models.DateField(default=None,null=True,blank=True, verbose_name='添加时间')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    del_time = models.DateTimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间',db_index=True)

    class Meta:
        verbose_name = verbose_name_plural = '帖子表'
        db_table = 'asset_info_table'

    @staticmethod
    def query_by_search(search, **kwargs):
        result = AssetInfoTable.objects.filter(del_time=None)
        contains = ["title","desc", "user_name","user_phone","company_name"]
        for b in contains:
            if b in search and search[b]:
                result = result.filter(**{b+"__contains": search[b]})
        check1 = ["number_id","c1","c2","sheng_id",
                  "front_sts","source","value","accept_man_id",
                  "shi_id","zone_id"
                  ]
        for w in check1:
            if w in search and search[w]:
                result = result.filter(**{w: search[w]})
        if 'start_time' in search and search['start_time']:
            startTime = datetime.datetime.strptime(search['start_time'], '%Y-%m-%d')
            result = result.filter(created_time__gte=startTime)
        if 'end_time' in search and search['end_time']:
            endTime = datetime.datetime.strptime(search['end_time'], '%Y-%m-%d') + datetime.timedelta(days=1)
            result = result.filter(created_time__lt=endTime)
        if "is_next" in search and search['is_next']:  # 获取下一条
            if "power_sts" in search and search["power_sts"]:
                result = result.filter(power_sts=search["power_sts"])
            index = (int(search['pageNumber'])-1)*int(search['pageSize'])+int(search['position'])
            total = result.count()
            if index >= total:
                return -1,-1, []  # 表示超出限制没有数据
            elif index < 0:
                return -2,-2, []
            else:
                data = result.order_by('-created_time')[index:index+1].values()
                return total,1, data

        else:
            others = result.values('power_sts').annotate(nums=Count('id'))

            if "power_sts" in search and search["power_sts"]:
                result = result.filter(power_sts=search["power_sts"])
            total = result.count()
            return total, others, result.order_by('-created_time').values()





