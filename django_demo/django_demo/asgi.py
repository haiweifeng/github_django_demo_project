"""
ASGI config for django_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import asyncio
import datetime
import json
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_demo.settings")
from src.Index.models import MyUsers

from urllib.parse import parse_qs
import aiormq
from django.core.asgi import get_asgi_application
from django_demo.settings import RABMQ_USERNAME, RABMQ_PASSWORD, RABMQ_HOST,logger,DEBUG
from django_redis import get_redis_connection
django_asgi_app = get_asgi_application()
conn = get_redis_connection('default')


async def sms_on_message(message):
    """
    异步消息存储到数据库
    """
    msg = json.loads(message.body)
    if msg.get('type') == 1:
        info = msg.get('info')
        phone = info.get("phone","")
        if phone:
            data = await MyUsers.objects.filter(phone=phone).afirst()
            if data:
                logger.info(f"{data.__dict__}")

    logger.info(f"{msg}")


async def mq_start():
    logger.info(f'mq_start-->去连接rabbitmq->{datetime.datetime.now()}')
    connection = await aiormq.connect(f"amqp://{RABMQ_USERNAME}:{RABMQ_PASSWORD}@{RABMQ_HOST}/")
    channel = await connection.channel()

    # Declaring queue
    declare_ok = await channel.queue_declare('asset', auto_delete=False)
    await channel.basic_consume(
        declare_ok.queue, sms_on_message, no_ack=True
    )

if not DEBUG:  # 部署时启动此处
    asyncio.create_task(mq_start())

async def application(scope, receive, send):
    # 测试可以在这里启动mq，加个锁也行
    # start_lock = conn.get('mq_start_lock')
    # if start_lock is None:
    #     conn.set('mq_start_lock', 1, 60*60)
    #     await mq_start()
    if scope['type'] == 'http':
        await django_asgi_app(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")


async def websocket_application(scope, receive, send):
    """socket 连接想用自己扩展吧"""
    while True:
        event = await receive()
        params = scope.get('query_string', "")
        p = parse_qs(params.decode('utf-8'))

        try:
            token = p['token'][0]
            user = json.loads(conn.get(token))
            if user:
                logger.info(f"{user}==>")
                # data = await MyUsers.objects.filter(id=user['id']).afirst()
                # logger.info(f"{data.name}==>data")
                if event['type'] == 'websocket.connect':
                    await send({
                        'type': 'websocket.accept'
                    })

                if event['type'] == 'websocket.disconnect':
                    break

                if event['type'] == 'websocket.receive':

                    if event['text'] == '发送数据':
                        await send({
                            'type': 'websocket.send',
                            'text': 'pong!'
                        })
        except:
            break
