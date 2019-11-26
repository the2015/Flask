# # encoding: utf-8
#
# from flask_socketio import emit  # 新加入的代码
# from threading import Lock
# import random
#
# # 新加入的代码-开始
# from App import socketio
#
# thread = None
# thread_lock = Lock()
# users_to_json = [{'name': 'yyf' + str(random.randint(1, 100))}]
#
#
# def background_thread(users_to_json):
#     """Example of how to send server generated events to clients."""
#     while True:
#         print(users_to_json)
#         users_to_json = [{'name': '王腾' + str(random.randint(1, 100))}]
#         socketio.sleep(0.5)  # 每五秒发送一次
#         socketio.emit('user_response', {'data': users_to_json}, namespace='/websocket/user_refresh')
#
#
# @socketio.on('connect', namespace='/websocket/user_refresh')
# def connect():
#     """ 服务端自动发送通信请求 """
#     global thread
#     user_to_json = ''
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread, (users_to_json,))
#     emit('server_response', {'data': '试图连接客户端！'})
#
#
# @socketio.on('connect_event', namespace='/websocket/user_refresh')
# def refresh_message(message):
#     """ 服务端接受客户端发送的通信请求 """
#     emit('server_response', {'data': message['data']})
# # 新加入的代码-结束

from flask import render_template, Blueprint
web = Blueprint('web', __name__)


@web.route('/')
def index():
    return render_template('test.html')


@web.route('/index1')
def index1():
    return render_template('index.html')
