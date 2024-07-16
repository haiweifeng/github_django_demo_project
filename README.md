# django_open_project

#### 介绍
练习两年半归来，我想试图教会你怎么用django写一个api后台
#### 写在前边的一些看法
1. 都说django慢，到底一个请求响应时间多久算慢呢。根据我的测试，一个请求响应时间大概在15ms左右，耗时的操作大部分是数据库。
2. 数据库耗时这块，django的慢主要在于count()，一百万count()大约在90ms，一千万条数据count()耗时大概在500ms左右(没用自增id，用的uuid)，count()在很多时候是可以优化的，如果是在觉得慢甚至可以写成固定值
3. 普通程序员开发的后台其实都是几百人在用，那你还等什么，用这一套开发开发速度很快，搭配上api文档，写一天摸4天鱼
4. 从懒人的角度来看，我认为当你写一个东西用上固定套路的时候，那你的工作肯定很轻松，有更多的时间放在学习，或者生活上



#### 常用的django命令
1. django-admin startproject django_demo 用于创建一个django项目
cd到django项目目录下创建src目录用于存放app，创建Login文件夹
2. python manage.py startapp Login src/Login # 用于创建Login app
3. python manage.py runserver # 启动django项目
4. python manage.py makemigrations # 生成迁移文件
5. python manage.py migrate # 执行迁移文件
6. python manage.py collectstatic # 静态文件收集


### 我的设计思路
1. 关于类视图的使用思路
```python
class MyUsersListView(ApiBaseView):
    """
    获取后台用户列表信息
    """
    model = MyUsers
    _keys = [('name', '用户姓名',""), ('phone', '手机号',"")]
    action_desc = "后台用户列表"
    schema = create_normal_schema(_keys,add_page=True,add_token=True)
```
一个基本的查询页无非就是获取查询参数，查询对应的数据库表格，然后返回给前端。使用django的类视图继承，可以减少重复代码，减少开发时间。
关于apiBaseView的设计根据你自己的大部分逻辑来统一设计，遇到特殊的情况，可以重写get放法自己定义。
同理，增加，编辑，删除，其实都是相似的动作，所以都可以继承。类视图很强大，对比fastapi什么的，你用多了你就懂了

2. 关于api文档的使用
create_schema 和create_normal_schema 两个方法都是为了创建api文档，create_normal_schema 是为了创建一个数据库中没有的参数，你需要自己
写schema,标明参数的含义和默认值，create_schema是创建一个数据库中有的参数，你只需要定义是否必填，要不要带个默认值。
add_token  请求是否带上token，add_page 是否需要分页参数 add_id 是否需要id参数 等等，你都可以自己定义
create_schema 元组长度为1时，默认是必填，长度大于1时，默认不是必填
```python
schema = create_normal_schema([('ids', '删除的id数组')], add_token=True)

key1 = [('name',), ('phone',), ('password',), ('account',)]
keys, schema = create_schema(MyUsers, key1,add_token=True)

```

3. 关于数据库查询操作
```python
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
```
apibaseview中，query_by_search方法就是用来查询数据库的，可以自己定义。通过重写get_data方法，可以指定查询的静态方法

4. 关于rabbitmq和socket的使用
我使用的django版本是5.0.6,启动方式默认daphne，所以走的是asgi模式,我把一些异步的方法都放在asgi.py中了，如果有需要自行放开使用

5. 关于异步的使用
```python
def post(self, request):
    vip_id = request.data.get('vip_id', '')
    print("vip",vip_id)
    after_task.after_response(vip_id)
    # my_signal.send(sender=vip_id, msg='Hello world')
    return json_res(code=200, msg=vip_id)
```
参看demo_test接口的使用方式，后续如果有需求也可以加上celery,反正目前没计划。我以前使用的都是celery,最近觉得这个可以试试。

6. 关于部署
环境包参考req.txt文件，使用supervisor部署项目，配置文件参考supervisor_conf中的配置文件。如果你不会用可以留言，我写个详细的教程

### 联系我
微信：harwen001 
如果有什么问题，欢迎留言交流，或者加我微信，一起学习。你要是真觉得这个项目帮助了你，也可以请我喝杯咖啡。![码在这](django_demo/media/1.jpg)