import os
import random
import threading
from threading import Lock

from flask import request, session, render_template
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_socketio import SocketIO, emit

from App import create_app
from ext import socketio

env = os.environ.get("FLASK_ENV", "develop")
app = create_app(env)

app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
thread = None
thread_lock = Lock()

manage = Manager(app=app)
manage.add_command('db', MigrateCommand)


def background_thread():
    count = 0
    while True:
        # print(threading.current_thread().getName())
        socketio.sleep(1)
        count += 1
        # socketio.emit('my_response',
        #               {'data': 'Server generated event', 'count': count},
        #               namespace='/test')


@socketio.on('my_event', namespace='/test')
def mtest_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


# @socketio.on('my_broadcast_event', namespace='/test')
# def mtest_broadcast_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)
#
#
# @socketio.on('join', namespace='/test')
# def join(message):
#     join_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})
#
#
# @socketio.on('leave', namespace='/test')
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})
#
#
# @socketio.on('close_room', namespace='/test')
# def close(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
#                          'count': session['receive_count']},
#          room=message['room'])
#     close_room(message['room'])
#
#
# @socketio.on('my_room_event', namespace='/test')
# def send_room_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          room=message['room'])
#
#
# @socketio.on('disconnect_request', namespace='/test')
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()
#
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']},
#          callback=can_disconnect)
#
#
# @socketio.on('my_ping', namespace='/test')
# def ping_pong():
#     emit('my_pong')


@socketio.on('connect', namespace='/test')
def mtest_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def mtest_disconnect():
    print('Client disconnected', request.sid)


manage.add_command('run', socketio.run(app=app, host='0.0.0.0', port=6001), threadad=True,
                   processes=2)  # 新加入的代码，重写manager的run命令

if __name__ == '__main__':
    # socketio.run(app, debug=True, port=8888)
    manage.run()


# LoadFile "e:/python3.7/python37.dll"
# LoadModule wsgi_module "e:/python3.7/lib/site-packages/mod_wsgi/server/mod_wsgi.cp37-win32.pyd"
# WSGIPythonHome "e:/python3.7"