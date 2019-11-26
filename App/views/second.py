import os
import queue
import time
from concurrent.futures.thread import ThreadPoolExecutor
from importlib import import_module
import cv2
from flask import Response, Blueprint
from ext import ToJsonStr
from send_msg import send_msg
from test import print_time

try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from App.BaseCamera import BaseCamera

q = queue.Queue()
blue2 = Blueprint('blue2', __name__)
video = cv2.VideoCapture(0)
filepath = "D:\\mypro\\pycharworkspace\\Flask\\"  # 模型数据图片目录os.listdir(os.path.abspath("../"))
face_detector = cv2.CascadeClassifier(
    "E:\PYTHON3.7\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")  # 级联检测器获取文件
face_thread = _threading.Thread(target=print_time)
thread_pool = ThreadPoolExecutor(2)


class VideoCamera(BaseCamera):

    @staticmethod
    def frames():
        count = 0
        while True:
            success, image = video.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 在灰度图像基础上实现的
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + w), (255, 0, 0))
                count += 1
                if count <= 1:
                    start = time.time()
                    send_msg(ToJsonStr(image.copy()))
                    print(time.time()-start)
                    # send_msg(json.dumps(image.copy().tolist()))
                    # print(send)
                    # print("-----------------------------")
                    # rec = np.array(json.loads(send), dtype=np.uint8)
                    # print(rec.dtype)
                    # custom(rec)
                    # print(image.tostring())
                    cv2.imwrite(filepath + "img/test/model.jpg", gray[y: y + h, x: x + w])
                else:
                    count = 0
            ret, jpeg = cv2.imencode('.jpg', image)
            yield jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@blue2.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
