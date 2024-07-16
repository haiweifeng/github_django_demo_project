import datetime
import json
import os, django
import uuid


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_demo.settings")
django.setup()

from src.tools.tools import md5_password
from src.Index.models import MyRoles,MyUsers

data = {
    "name": "测试",
    "phone": "123456789012",
    "password": md5_password("Aa123456"),
    "account": "admin",
}

MyUsers.objects.create(**data)
print("创建成功")