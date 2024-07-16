#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 用于测试rabbitmq的消息接受功能，手动运行发送消息
import asyncio
import json

import aiormq

from django_demo.settings import RABMQ_USERNAME, RABMQ_PASSWORD, RABMQ_HOST, RABMQ_PORT


async def send_rabbitmq(title,msg=''):
    connection = await aiormq.connect(f"amqp://{RABMQ_USERNAME}:{RABMQ_PASSWORD}@{RABMQ_HOST}:{RABMQ_PORT}/")
    channel = await connection.channel()

    body = msg.encode()
    await channel.queue_declare(title, auto_delete=False)

    await channel.basic_publish(body, routing_key=title)
    await connection.close()

#

info = {'info': {'uid': '20111', 'name': '姓名', 'phone': '18831182123', 'comname': '公司名字',}, 'type': 1}


msg = json.dumps(info)
title = "test_demo"
asyncio.run(send_rabbitmq(title,msg))
