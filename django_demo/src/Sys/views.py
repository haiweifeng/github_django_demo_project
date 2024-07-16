import datetime
import re
from src.Index.models import MyUsers
from src.tools.base_view import ApiBaseView, ApiAddView, ApiEditView, ApiDelView, create_normal_schema, create_schema
from src.tools.tools import md5_password


class MyUsersListView(ApiBaseView):
    """
    获取后台用户列表信息
    """
    model = MyUsers
    _keys = [('name', '用户姓名',""), ('phone', '手机号',"")]
    action_desc = "后台用户列表"
    schema = create_normal_schema(_keys,add_page=True,add_token=True)


class MyUsersAddView(ApiAddView):
    """
        后台用户的添加
    """
    model = MyUsers
    action_desc = "后台用户添加"
    uniq = 'phone'
    checked = True
    key1 = [('name',), ('phone',), ('password',), ('account',)]
    keys, schema = create_schema(MyUsers, key1,add_token=True)

    @staticmethod
    def keys_check(req):
        # 用于检测字段类型的正确性
        if not req.data.get('name', ''):
            return True, '姓名不可为空！'
        if not re.match(r"^1[3456789]\d{9}$", req.data.get('phone', '')):
            return True, '手机号格式错误！'
        return False, 'success'

    @staticmethod
    def check_sth(request,data):
        data['password'] = md5_password(data['password'])
        return True, data


class MyUsersEditView(ApiEditView):
    """
    后台用户的编辑
    """
    model = MyUsers
    action_desc = "后台用户编辑"
    uniq = 'phone'
    key1 = [('name',), ('phone',), ('password',"")]
    keys, schema = create_schema(MyUsers, key1, add_token=True,add_id=True)

    @staticmethod
    def keys_check(req):
        # 用于检测字段类型的正确性
        if not re.match(r"^1[3456789]\d{9}$", req.data.get('phone', '')):
            return True, '手机号格式错误！'
        return False, 'success'

    @staticmethod
    def check_sth(request,data):
        data.update({'update_time': datetime.datetime.now()})
        pwd = data.get("password", "")

        if pwd:
            data['password'] = md5_password(data['password'])
        else:
            if "password" in data:
                del data['password']
        return True, data


class MyUsersRemoveView(ApiDelView):
    """
    后台用户删除  ids []
    """
    model = MyUsers
    action_desc = "后台用户删除"

