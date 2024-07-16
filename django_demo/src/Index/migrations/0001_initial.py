# Generated by Django 5.0.6 on 2024-07-15 09:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AssetInfoTable",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="帖子标题",
                    ),
                ),
                (
                    "desc",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="帖子描述"
                    ),
                ),
                (
                    "user_name",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="联系人"
                    ),
                ),
                (
                    "user_phone",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="电话"
                    ),
                ),
                (
                    "source",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True, verbose_name="来源类型"
                    ),
                ),
                (
                    "front_sts",
                    models.PositiveIntegerField(
                        blank=True, default=1, null=True, verbose_name="前台状态"
                    ),
                ),
                (
                    "cycle",
                    models.PositiveIntegerField(
                        blank=True, default=1, null=True, verbose_name="周期"
                    ),
                ),
                (
                    "source_record_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="各种来源的记录id",
                    ),
                ),
                (
                    "accept_man_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="申领人id",
                    ),
                ),
                (
                    "accept_man_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="申领人name",
                    ),
                ),
                (
                    "accept_time",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="申领时间"
                    ),
                ),
                (
                    "number_id",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="数字id",
                    ),
                ),
                (
                    "power_sts",
                    models.PositiveIntegerField(
                        blank=True, default=1, null=True, verbose_name="状态"
                    ),
                ),
                (
                    "sheng_id",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="省ID",
                    ),
                ),
                (
                    "shi_id",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="市ID",
                    ),
                ),
                (
                    "zone_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="区id",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="地址",
                    ),
                ),
                (
                    "week",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="周",
                    ),
                ),
                (
                    "cate_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="分类全称",
                    ),
                ),
                (
                    "c1",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="类别1",
                    ),
                ),
                (
                    "c2",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="类别2",
                    ),
                ),
                (
                    "c3",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="类别3",
                    ),
                ),
                (
                    "vol",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="处置量",
                    ),
                ),
                (
                    "unit",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="单位",
                    ),
                ),
                (
                    "images",
                    models.TextField(
                        blank=True,
                        default="",
                        null=True,
                        verbose_name="图片数组-前端转为json字符串",
                    ),
                ),
                (
                    "video_url",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="视频url"
                    ),
                ),
                (
                    "key_words",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="关键词"
                    ),
                ),
                (
                    "labels",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="标签"
                    ),
                ),
                (
                    "value",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True, verbose_name="价值判定"
                    ),
                ),
                (
                    "valuation",
                    models.PositiveIntegerField(
                        blank=True, default=8, null=True, verbose_name="估值"
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="公司名称",
                    ),
                ),
                (
                    "com_sheng_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="省ID",
                    ),
                ),
                (
                    "com_shi_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="市ID",
                    ),
                ),
                (
                    "com_zone_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="区id",
                    ),
                ),
                (
                    "com_address",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="地址",
                    ),
                ),
                (
                    "industry",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="所属行业",
                    ),
                ),
                (
                    "industry_id",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True, verbose_name="行业id"
                    ),
                ),
                (
                    "remark",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="备注"
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        blank=True, default=None, null=True, verbose_name="有效截止日期"
                    ),
                ),
                (
                    "add_time",
                    models.DateField(
                        blank=True, default=None, null=True, verbose_name="添加时间"
                    ),
                ),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[(1, "正常"), (0, "删除")], default=1, verbose_name="状态"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "del_time",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "帖子表",
                "verbose_name_plural": "帖子表",
                "db_table": "asset_info_table",
            },
        ),
        migrations.CreateModel(
            name="MyRoles",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="角色名称",
                    ),
                ),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[(1, "正常"), (0, "删除")], default=1, verbose_name="状态"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "del_time",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "角色表",
                "verbose_name_plural": "角色表",
                "db_table": "my_roles",
            },
        ),
        migrations.CreateModel(
            name="MyUsers",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "number_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="数字id",
                    ),
                ),
                (
                    "account",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="账号",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="用户姓名",
                    ),
                ),
                (
                    "head_img",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=128,
                        null=True,
                        verbose_name="头像",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=16,
                        null=True,
                        verbose_name="手机号",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="密码",
                    ),
                ),
                (
                    "log_ip",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="登陆ip",
                    ),
                ),
                (
                    "log_time",
                    models.DateTimeField(blank=True, null=True, verbose_name="登陆时间"),
                ),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[(1, "正常"), (0, "删除")], default=1, verbose_name="状态"
                    ),
                ),
                (
                    "del_time",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "用户表",
                "verbose_name_plural": "用户表",
                "db_table": "my_users",
            },
        ),
        migrations.CreateModel(
            name="NumberRoles",
            fields=[
                (
                    "id",
                    models.AutoField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=64,
                        null=True,
                        verbose_name="角色名称",
                    ),
                ),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[(1, "正常"), (0, "删除")], default=1, verbose_name="状态"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "del_time",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="创建时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "测试数字id角色表",
                "verbose_name_plural": "测试数字id角色表",
                "db_table": "number_roles",
            },
        ),
    ]