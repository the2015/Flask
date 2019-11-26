#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
from concurrent.futures.thread import ThreadPoolExecutor

import pika
from gevent import thread

from ext import Tondarray, parse, lock
from test import custom

credentials = pika.PlainCredentials('guest', 'guest')
hostname = 'localhost'
parameters = pika.ConnectionParameters(hostname, credentials=credentials)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
queue = channel.queue_declare(queue='queuetest')
thread_pool = ThreadPoolExecutor(2)


def callback(ch, method, properties, body):
    t = thread_pool.submit(executor, body)
    t.add_done_callback(parse)
    # thread_pool.shutdown(wait=True)


def executor(arg):
    lock.acquire()
    arr = Tondarray(arg)
    custom(arr)


# 告诉rabbitmq使用callback来接收信息
# channel.basic_consume(callback, queue='hello', no_ack=True)
channel.basic_consume("queuetest", callback, consumer_tag="queuetest", auto_ack=True)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理,按ctrl+c退出
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
