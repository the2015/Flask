import pika

credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
connection = pika.BlockingConnection(parameters)  # 连接 RabbitMQ

channel = connection.channel()  # 创建频道

queue = channel.queue_declare(queue='queuetest')  # 声明或创建队列


def send_msg(arg):
    channel.basic_publish(exchange='exchangetest',
                          routing_key='rkeytest',
                          body=arg)


def check_msg_count():
    # 检查队列，以重新得到消息计数
    queue = channel.queue_declare(queue='queuetest', passive=True)
    '''
     queue.method.message_count 获取的为 ready 的消息数
     walker 没找到利用 pika 获取 unack 或者 total 消息数的方法  
    '''
    messageCount = queue.method.message_count
    print('messageCount: %d' % messageCount)
    if messageCount > 100:
        connection.sleep(1)


# 关闭连接
def close_connettion():
    connection.close()
